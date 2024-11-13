import json
import re
from collections import Counter, defaultdict

import nltk
from dask.array import negative
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_all_english(sentence):
    return bool(re.match(r'^[a-zA-Z\s]+$', sentence))

def clean_review(review):
    # 去掉无用的信息
    lines = review.strip().split('\n')
    #print("-------------------------original----------------------------------")
    #print(lines)
    del lines[0] #short cut
    commenter = lines.pop(0)
    region = lines.pop(0)
    room_level = lines.pop(0)
    room_night = lines.pop(0)
    members = lines.pop(0)
    score = 0
    comment_content = []
    for line in lines:
        if "There are no comments available for this review" in line:
            continue
        elif "Reviewers choice" in line or "Reviewed" in line:
            continue
        elif "Scored" in line:
            score = float(line.split(" ")[1])
        elif line.isdigit() or is_float(line):
            score = float(line)
        elif "Helpful" in line or "Not helpful" in line or "found this review helpful" in line:
            continue
        else:
            comment_content.append(line.strip())
    processed_result = {"commenter":commenter,"region":region,"room_level":room_level,"room_night":room_night,"members":members,"score":score,"comment_content":comment_content}
    print("---------------------------------------process----------------------------------------------------")
    return processed_result


def analyze_sentiment(review):
    blob = TextBlob(review)
    sentiment = blob.sentiment.polarity

    return sentiment


def extract_nouns(review):
    tokens = word_tokenize(review)
    tagged = pos_tag(tokens)
    nouns = [word for word, pos in tagged if pos in ['NN', 'NNS']] #'NNP', 'NNPS']]不要專有名詞了
    return nouns

def remove_supersets(nouns):
    nouns = set(nouns)
    to_remove = set()

    for noun in nouns:
        for other in nouns:
            if noun != other and noun in other:
                # 如果 noun 是 other 的子集且二者不同，则移除较长的那个
                to_remove.add(other)

    return nouns - to_remove


if __name__ == '__main__':
    #nouns = {'adjacent', 'instruction', 'wait', '枕頭', 'es', 'decade', 'spa', '超級市場', 'kunnen', 'products', 'tranquilo', 'need', 't he', 'både', 'cash', '火車站', 'plug', '吹髮器', 'mehr', 'bit', 'rail', 'rochen', 'entrance', '공간', 'grün', 'muf', 'und', 'milk', '百貨', '恐怖', 'MRT', 'call', 'bra', 'wasn', 'policy', 'range', 'helt', 'specific', '便利店', '一次付清', '床', 'club', 'face', '泳池', '有點擔心', 'je', 'dentro', '편리하고', 'tiene', 'zwembad', '入住', 'sengen', 'tot', '住宿', 'pool', 'rice', 'buurt', 'bij', '住客', 'job', 'wife', 'office', 'Bad', 'guards', '房间', 'geweldig', '日本人', 'ideaal', 'tijdens', 'lobby', 'morning', 'back', 'på', 'colours', 'bien', 'stay', '沙發', 'walk', 'staff', 'hi', '咖啡', 'wise', '消毒液', 'lock', 'close', '機場', 'sense', 'choice', 'pot', 'girl', 'aan', 'air', 'peice', '快適', 'fräscht', 'més', 'neck', 'slice', '舒服', 'nära', 'climatisation', 'locatie', '气味', 'vi', 'well', 'check', '除臭劑', '有一點菸味', 'exit', 'Prima', '花灑', '電視', 'Rien', 'sofa', 'pillow', '满足需求', 'hygiënisch', 'hård', 'Check', 'midden', 'luxury', '大堂', '吓洪', '有問有答', 'masayas様', '员工', 'mold', 'die', '😜', '，big', '寄存行李', '樓層', 'trip', 'wir', 'fijn', '冷氣', 'druk', 'son', 'lift', 'cup', 'Lobby', 'gel', 'firm', 'Geweldig', '很棒', '職員', 'couloirs', 'sehr', 'sorts', 'one', 'expectation', 'ceiling', '센트럴', 'cell', 'station', 'ammo', 'skills', 'bag', '裝修', '傢俱', '편함', 'fint', 'building', 'wassen', 'end', 'package', 'formatge', 'clinic', 'byen', 'fold', 'heaps', 'stool', 'STAff', 'line', 'luggage', 'exception', 'paar', 'penny', 'lätt', 'work', 'groß', '总体来说挺好的', 'nvt', 'safe', 'río', 'criticism', 'graden', '거에요', 'go', '性价比', 'vatbaar', 'use', '水', 'altijd', '有禮貌', 'Pool', 'diligent', 'blunt', 'night', 'front', 'smelt', 'e.g', '！！', 'täglich', 'een', 'help', 'bridge', 'Connects', 'cross', 'light', '特大房', 'tv', 'molt', 'storage', 'vor', 'เซอร์วิตควรปรับปรุงให้มากกว่านี้', 'twin', 'memory', 'finish', 'car', 'world', 'panel', 'ถูกใจมาก', 'depan', 'toys', 'sum', 'vague', '体验', 'bay', 'smell', 'wifi', 'biscuits', 'Nice', 'deilig', '👍👍👍', 'gab', 'prospect', 'pickups', 'madrassen', 'spray', 'cost', '一次就夠', 'sarapan', 'ride', 'kid', '直播', 'Enjoy', 'ไม่มีฟิตและสระว่ายน้ำให้บริการและควรมีคนมาช่วยลูกค้ายกกระเป๋าด้วย', 'gifts', 'gigantische', '差', '浴室', 'time', 'sentrum', 'до', 'ke', 'ein', '設施', 'heisen', 'course', 'säng', 'ทําเลและที่พักสะอาดมากพนักงานทุกคนมารยาทดีมาก', 'op', 'Car', 'cot', '尊敬', 'proof', 'maid', '錢', 'Etage', 'fan', 'dinámico', 'allt', 'seats', 'frukost', '費事出聲', '非常好', '价格', 'โดยรวมดีพนักงานที่พูดจาและให้ความช่วยเหลือดี', 'life', '不足夠用', 'Pillows', 'ganz', '整體', 'pub', 'city', 'group', 'man', '前台', 'обновили', 'OK', 've', 'link', '加購', '禁煙房', 'dining', 'cinema', 'men', 'extras', '可以接受', '너무만족스러움', '☹️', 'base', 'tiefe', '早餐', 'bei', 'w.cheung', 'tai', 'seltsam', 'væk', '生果及蛋不足', '窩心之旅', 'photo', '插蘇位', '服务', 'días', '商場', 'gb', '관광지와', '房間', '發霉', 'vacation', 'le', '飯店', 'peu', 'royal', 'case', '酒店', 'forhånd', 'cockroach', 'Номера', 'seals', 'centrum', '比較舊', "l'amabilitat", '舒适', '香港', 'liquid', '좋겠음', 'para', '套餐', 'Food', 'kong', 'on/off', 'noise', 'count', 'faltar', 'stort', '客人', 'buggy', 'vänja', '😀', 'köp', 'war', 'typhoon', 'ha', 'monitor', 'mit', 'cycling', 'Man', 'usage', 'behulpzaam', 'voor', 'jg', 'amazing', '空間', 'speedy', 'bed', 'sq', 'för', 'dust', 'Tv', 'right', '物超所值', 'badrum', '服務', 'tan', 'brush', 'till', 'praise', '有點早', 'et', 'vært', 'tid', '位置', 'couldn', '疫情', 'YYM', 'client', 'Meals', '风景', '早上', 'pm', 'choon，', 'noisy', '去年', 'efficiency', 'dine', 'tin', 'vue', '整修', '都很好', '清潔', 'xiuping', '美中不足', 'king', 'riecht', 'ทำเลสะดวก', 'towel', '😊', 'jacky', 'Staff', '空调', 'act', 'juga', 'si', 'ben', 'loan', 'school', '制冷', 'Lack', 'quality', '味道', 'min', '적합', 'tip', 'traffic', 'maar', 'function', 'deur', '房门', '吸煙房', 'fast', 'lunch', '装修', 'plumb', '另外', 'rack', 'bin', 'flush', 'moulds', 'familie', 'gingen', 'pas', 'hour', '设施', 'koffie', '河景', 'dim', 'bar', '家庭', 'couch', 'aspect', '押金', 'ask', '奶瓶', '廁所', 'våningar', 'trotzdem', 'fuk', 'upgrade', 'art', 'dit', 'van', 'voice', 'location', 'расположение', 'gaf', 'point', 'wash', 'tussen', '청결', 'soepel', 'chloorsmaak', 'meat', 'privacy', 'rigtig', 'plus', 'må', 'ok', 'load', 'bulk', 'cabs', 'Ok', 'fee', 'iron', 'Xuan', '還不錯', '一般', 'da', 'star', '蓮蓬頭', '分隔', 'tub', '下雨', '下次', '商场', 'var', 'week', 'ppl', 'issue', 'disruption', 'muss', 'públic', 'Lifts', 'buchen', 'way', 'mall', 'groot', 'toen', 'Dear', 'drying', 'inn', '洗手間', 'rude', 'noice', 'Nil', 'swim', 'lys', '가깝고', 'alojaron', 'cold', 'klær', '游泳馆', 'fault', 'fort', 'ideal', 'ons', '嬰兒', 'year', 'gran', '없어요', '🔥', '不会再選', 'auf', 'family', '지하철', 'für', 'adequaat', 'skin', '環境', 'cap', 'foot', 'drink', '外面', '整潔', 'la', 'arrival', 'von', 'mooi', 'hygiëne', 'Beds', 'tunnel', 'Rengørings', 'ist', '隔音', 'pricy', '比價性', 'hub', 'cool', 'ruim', 'baby', '員工', 'fruit', 'ショッピングモールが近く、非常に便利', '空气', 'Efficient', 'kort', 'lot', '客服', 'search', '人員', 'con', '駅', '安静', '수영장이크고', 'type', 'self', 'mtr', 'og', 'ut', '거리가있음', 'knuffels', '寬闊', 'litt', 'Yin，', '舒適', 'didn', 'hospitality', '卫生', '🤗', '尾房', 'nicht', 'eg', 'nurse', 'chengjin', 'av', 'TV', 'decor', 'stuff', 'søde', 'speciellt', 'meal', 'bell', 'floor', 'value', 'N.A', 'journey', 'app', '感觉不错', '🥰🥰🥰🥰🥰🥰', '斷線嚴重', '時間', 'hygiene', 'obligatory', 'waar', '方便', 'soap', 'とても満足', 'schoon', 'Location', 'food', 'mig', '很滿意', '环境', 'cast', '聞', '호텔', 'facility', 'heat', 'rain', 'port', 'très', '満足しました．', 'โดยรวมพนักงานมารยาทดีและให้ความช่วยเหลือดี', 'accident', 'nydelig', '没有', 'MTR', '冇', 'mum', 'in快', 'park', 'samme', 'gehorig', 're', 'Noisy', 'que', 'speck', '健身室', 'zijn', 'wall', 'bus', 'multitude', 'arm', '嘈', 'notice', 'draws', '空調', 'kan', 'hk', 'noe', 'Reception', 'fridge', 'så', 'heeft', 'coz', 'kind', '浴缸', 'ze', '很不錯', 'taxi', 'town', 'localisation', 'hebt', 'att', 'mood', '打掃', 'kowloon', 'meaning', 'er', 'katie', '價格', 'ae', 'แม่บ้านทําความสะอาดห้องไม่สะอาดเป็นบ้างค้างต้องให้บอก', '地點', 'zwei', 'fumar', '失望', 'gem', '干凈', 'dusch', 'Lights', '櫃台', 'flowing', 'Porion', 'suits', 'Simon', 'limpia', 'PERFECT', 'guys', '插頭', 'dino', 'yan', 'cans', 'gym', 'gripe'}
    #removed_nouns = remove_supersets(nouns)
    #print(removed_nouns)

    nltk.download("punkt")
    nltk.download('averaged_perceptron_tagger')
    with open("./resources/hotel_reviews.json", "r", encoding="utf-8") as file:
        # 从文件中加载JSON数据
        comment_reviews = json.load(file)
    result = {}
    all_adjective = set()
    adjective_classify = {'positive': ['comfortable', 'Rewelacja', 'Excellent', 'Definitely recommend', 'waanzinnige ervaring', 'OK', 'Fantastyczne miejsce', 'Fajnie', 'Very Good', 'Decent stay', 'good value', 'Good', 'Great relaxation', 'excellent', 'excellent staffs', 'Happy', 'Odlican hotel', 'Wonderful', 'Super', 'Fair', 'Comfortable stay', 'Exceptional', 'Fantastic', 'Friendly staffs', 'Lovely cruise', 'udany weekend', 'Marvelous', 'Surprisingly good', 'Pleasant', 'Stupendo', 'very good'], 'negative': ['Bad', 'Very Poor', 'Poor', 'Disappointing']}

    all_adjective_counts = {}
    all_noun_classify ={}

    for hotel, reviews in comment_reviews.items():
        all_reviews = []
        all_nouns = {'adjacent', 'instruction', 'wait', '枕頭', 'decade', 'spa', '超級市場', 'kunnen', 'products', 'tranquilo', 'need', 'både', 'cash', '火車站', 'plug', '吹髮器', 'mehr', 'bit', 'rail', 'rochen', 'entrance', '공간', 'grün', 'muf', 'und', 'milk', '百貨', '恐怖', 'MRT', 'call', 'bra', 'wasn', 'policy', 'range', 'helt', 'specific', '便利店', '一次付清', '床', 'club', 'face', '泳池', '有點擔心', 'je', 'dentro', '편리하고', 'tiene', 'zwembad', '入住', 'sengen', 'tot', '住宿', 'pool', 'rice', 'buurt', '住客', 'job', 'wife', 'office', 'Bad', 'guards', '房间', 'geweldig', '日本人', 'ideaal', 'tijdens', 'lobby', 'morning', 'back',  'colours', 'bien', 'stay', '沙發', 'walk', 'staff',  '咖啡', 'wise', '消毒液', 'lock', 'close', '機場', 'sense', 'choice', 'pot', 'girl', 'aan', 'air', 'peice', '快適', 'fräscht', 'més', 'neck', 'slice', '舒服', 'nära', 'climatisation', 'locatie', '气味', 'well', 'check', '除臭劑', '有一點菸味', 'exit', 'Prima', '花灑', '電視', 'Rien', 'sofa', 'pillow', '满足需求', 'hygiënisch', 'hård', 'Check', 'midden', 'luxury', '大堂', '吓洪', '有問有答', 'masayas様', '员工', 'mold', 'die', '😜', 'big', '寄存行李', '樓層', 'trip',  'fijn', '冷氣', 'druk', 'son', 'lift', 'cup', 'Lobby', 'gel', 'firm', 'Geweldig', '很棒', '職員', 'couloirs', 'sehr', 'sorts', 'one', 'expectation', 'ceiling', '센트럴', 'cell', 'station', 'ammo', 'skills', 'bag', '裝修', '傢俱', '편함', 'fint', 'building', 'wassen', 'end', 'package', 'formatge', 'clinic', 'byen', 'fold', 'heaps', 'stool', 'STAff', 'line', 'luggage', 'exception', 'paar', 'penny', 'lätt', 'work', 'groß', '总体来说挺好的', 'nvt', 'safe', 'río', 'criticism', 'graden', '거에요',  '性价比', 'vatbaar', 'use', '水', 'altijd', '有禮貌', 'Pool', 'diligent', 'blunt', 'night', 'front', 'smelt',   'täglich', 'help', 'bridge', 'Connects', 'cross', 'light', '特大房', 'tv', 'molt', 'storage', 'vor', 'เซอร์วิตควรปรับปรุงให้มากกว่านี้', 'twin', 'memory', 'finish', 'car', 'world', 'panel', 'ถูกใจมาก', 'depan', 'toys', 'sum', 'vague', '体验', 'bay', 'smell', 'wifi', 'biscuits', 'Nice', 'deilig', '👍👍👍', 'gab', 'prospect', 'pickups', 'madrassen', 'spray', 'cost', '一次就夠', 'sarapan', 'ride', 'kid', '直播', 'Enjoy', 'ไม่มีฟิตและสระว่ายน้ำให้บริการและควรมีคนมาช่วยลูกค้ายกกระเป๋าด้วย', 'gifts', 'gigantische', '差', '浴室', 'time', 'sentrum', 'до', '設施', 'heisen', 'course', 'säng', 'ทําเลและที่พักสะอาดมากพนักงานทุกคนมารยาทดีมาก',  'Car', 'cot', 'proof', 'maid', '錢', 'Etage', 'fan', 'dinámico', 'seats', 'frukost', '費事出聲', '非常好', '价格', 'โดยรวมดีพนักงานที่พูดจาและให้ความช่วยเหลือดี', 'life', '不足夠用', 'Pillows', 'ganz', '整體', 'pub', 'city', 'group', 'man', '前台', 'обновили', 'OK',  'link', '加購', '禁煙房', 'dining', 'cinema', 'men', 'extras', '可以接受', '너무만족스러움', '☹️', 'base', 'tiefe', '早餐', 'bei', 'w.cheung', 'tai', 'seltsam', 'væk', '生果及蛋不足', '窩心之旅', 'photo', '插蘇位', '服务', 'días', '商場', '관광지와', '房間', '發霉', 'vacation', '飯店', 'peu', 'royal', 'case', '酒店', 'forhånd', 'cockroach', 'Номера', 'seals', 'centrum', '比較舊', "l'amabilitat", '舒适', '香港', 'liquid', '좋겠음', 'para', '套餐', 'Food', 'kong', 'on/off', 'noise', 'count', 'faltar', 'stort', '客人', 'buggy', 'vänja', '😀', 'köp', 'war', 'typhoon', 'monitor', 'mit', 'cycling', 'Man', 'usage', 'behulpzaam', 'voor', 'amazing', '空間', 'speedy', 'bed',  'för', 'dust', 'Tv', 'right', '物超所值', 'badrum', '服務', 'tan', 'brush', 'till', 'praise', '有點早', 'vært', 'tid', '位置', 'couldn', '疫情', 'YYM', 'client', 'Meals', '风景', '早上', 'choon，', 'noisy', '去年', 'efficiency', 'dine', 'tin', 'vue', '整修', '都很好', '清潔', 'xiuping', '美中不足', 'king', 'riecht', 'ทำเลสะดวก', 'towel', '😊', 'jacky', 'Staff', '空调', 'act', 'juga', 'si', 'ben', 'loan', 'school', '制冷', 'Lack', 'quality', '味道', 'min', '적합', 'tip', 'traffic', 'maar', 'function', 'deur', '房门', '吸煙房', 'fast', 'lunch', '装修', 'plumb', '另外', 'rack', 'bin', 'flush', 'moulds', 'familie', 'gingen', 'pas', 'hour', '设施', 'koffie', '河景', 'dim', 'bar', '家庭', 'couch', 'aspect', '押金', 'ask', '奶瓶', '廁所', 'våningar', 'trotzdem', 'fuk', 'upgrade', 'art', 'dit', 'van', 'voice', 'location', 'расположение', 'gaf', 'point', 'wash', 'tussen', '청결', 'soepel', 'chloorsmaak', 'meat', 'privacy', 'rigtig', 'plus', 'må', 'ok', 'load', 'bulk', 'cabs', 'Ok', 'fee', 'iron', 'Xuan', '還不錯', '一般', 'star', '蓮蓬頭', '分隔', 'tub', '下雨', '下次', '商场', 'var', 'week', 'ppl', 'issue', 'disruption', 'muss', 'públic', 'Lifts', 'buchen', 'way', 'mall', 'groot', 'toen', 'Dear', 'drying', 'inn', '洗手間', 'rude', 'noice', 'Nil', 'swim', 'lys', '가깝고', 'alojaron', 'cold', 'klær', '游泳馆', 'fault', 'fort', 'ideal', 'ons', '嬰兒', 'year', 'gran', '없어요', '🔥', '不会再選', 'auf', 'family', '지하철', 'für', 'adequaat', 'skin', '環境', 'cap', 'foot', 'drink', '外面', '整潔', 'la', 'arrival', 'von', 'mooi', 'hygiëne', 'Beds', 'tunnel', 'Rengørings', 'ist', '隔音', 'pricy', '比價性', 'hub', 'cool', 'ruim', 'baby', '員工', 'fruit', 'ショッピングモールが近く、非常に便利', '空气', 'Efficient', 'kort', 'lot', '客服', 'search', '人員', 'con', '駅', '安静', '수영장이크고', 'type', 'self', 'mtr', 'og', 'ut', '거리가있음', 'knuffels', '寬闊', 'Yin，', '舒適', 'didn', 'hospitality', '卫生', '🤗', '尾房', 'nicht',  'nurse', 'chengjin', 'av', 'TV', 'decor', 'stuff', 'søde', 'speciellt', 'meal', 'bell', 'floor', 'value', 'journey', 'app', '感觉不错', '🥰🥰🥰🥰🥰🥰', '斷線嚴重', '時間', 'hygiene', 'obligatory', 'waar', '方便', 'soap', 'とても満足', 'schoon', 'Location', 'food', 'mig', '很滿意', '环境', 'cast', '聞', '호텔', 'facility', 'heat', 'rain', 'port', 'très', '満足しました．', 'โดยรวมพนักงานมารยาทดีและให้ความช่วยเหลือดี', 'accident', 'nydelig', '没有', 'MTR', '冇', 'mum', 'in快', 'park', 'samme', 'gehorig',  'Noisy', 'que', 'speck', '健身室', 'zijn', 'wall', 'bus', 'multitude', 'arm', '嘈', 'notice', 'draws', '空調', 'kan', 'hk', 'noe', 'Reception', 'fridge',  'heeft', 'coz', 'kind', '浴缸', 'ze', '很不錯', 'taxi', 'town', 'localisation', 'hebt', 'mood', '打掃', 'kowloon', 'meaning',  'katie', '價格', 'แม่บ้านทําความสะอาดห้องไม่สะอาดเป็นบ้างค้างต้องให้บอก', '地點', 'zwei', 'fumar', '失望', 'gem', '干凈', 'dusch', 'Lights', '櫃台', 'flowing', 'Porion', 'suits', 'Simon', 'limpia', 'PERFECT', 'guys', '插頭', 'dino', 'yan', 'cans', 'gym', 'gripe'}

        adjective_counts = defaultdict(lambda: {"count": 0, "senti": ""})
        reviews_related_nouns = defaultdict(lambda: [])


        for review in reviews:
            cleaned_review = clean_review(review)
            print(cleaned_review)
            if len(cleaned_review["comment_content"]) == 1 and is_all_english(cleaned_review["comment_content"][0]) and len(cleaned_review["comment_content"][0].split(" ")) <= 2:
                # all_adjective.add(cleaned_review["comment_content"][0])
                comment = cleaned_review["comment_content"][0]
                if comment in adjective_classify["positive"]:
                    adjective_counts[comment]["count"] += 1
                    adjective_counts[comment]["senti"] = "positive"
                    continue

                elif comment in adjective_classify["negative"]:
                    adjective_counts[comment]["count"] += 1
                    adjective_counts[comment]["senti"] = "negative"
                    continue

            if cleaned_review:
                for line in cleaned_review["comment_content"]:
                    recombine_review = {"comment": line, "senti": "positive",
                                        "info": {"commenter": cleaned_review["commenter"],
                                                 "region": cleaned_review["region"],
                                                 "room_level": cleaned_review["room_level"],
                                                 "room_night": cleaned_review["room_night"],
                                                 "members": cleaned_review["members"],
                                                 "score": cleaned_review["score"]}}

                    sentiment = analyze_sentiment(line)
                    if sentiment >= 0:
                        recombine_review["senti"] = "positive"
                        all_reviews.append(recombine_review)
                    else:
                        recombine_review["senti"] = "negative"
                        all_reviews.append(recombine_review)
                    """
                    extracted_nouns = extract_nouns(line)
                    for noun in extracted_nouns:
                        all_nouns.add(noun)
                    """

        # 转换为所需格式
        adjective_comment_count = [{"name": adj, "count": count_info["count"], "senti": count_info["senti"]}
                                   for adj, count_info in adjective_counts.items()]

        print(adjective_comment_count)
        all_adjective_counts[hotel] = adjective_comment_count

        for noun in all_nouns:
            for review in all_reviews:
                if noun in review["comment"]:
                    reviews_related_nouns[noun].append(review)

        noun_comment_classify = [{"name": noun, "reviews": reviews} for noun, reviews in reviews_related_nouns.items()]

        print(noun_comment_classify)
        all_noun_classify[hotel] = noun_comment_classify

    with open("hotel_reviews_adjective.json", "w", encoding="utf-8") as f:
        json.dump(all_adjective_counts, f, ensure_ascii=False, indent=4)

    with open("hotel_reviews_noun.json", "w", encoding="utf-8") as f:
        json.dump(all_noun_classify, f, ensure_ascii=False, indent=4)
"""

    print(all_adjective)
    adjective_senti = {x:analyze_sentiment(x) for x in all_adjective}
    print(adjective_senti)
    adjective_classify = {"positive":[],"negative":[]}
    for adj in all_adjective:
        if adjective_senti[adj] >= 0:
            adjective_classify["positive"].append(adj)
        else:
            adjective_classify["negative"].append(adj)

    print(adjective_classify)

            if cleaned_review:
                sentiment = analyze_sentiment(cleaned_review)
                all_reviews.append({'review': cleaned_review, 'sentiment': sentiment})
                nouns = extract_nouns(cleaned_review)
                all_nouns.extend(nouns)
    
        # 统计名词
        noun_counts = Counter(all_nouns).most_common(10)
        noun_list = [noun for noun, count in noun_counts]

        # 生成最终 JSON 数据结构
        result[hotel] = {
            'nouns': noun_list,
            'reviews': all_reviews
        }
        # 输出结果
    result_json = json.dumps(result, ensure_ascii=False, indent=2)
    print(result_json)
"""
