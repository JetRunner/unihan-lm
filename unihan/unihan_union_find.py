import sys


def decode_unicode(code):
    if code.startswith('U+'):
        code = code[2:]
    return chr(int(code.split('<')[0], 16))


def get_vocabs(vocab_path):
    f = open(vocab_path)
    l = []
    for line in f:
        l.append(line.strip().split()[0])

    return l


def char_to_id(file_path='./Unihan_Variants.txt'):
    vocabs = get_vocabs()
    f = open(file_path)
    d, d_r = {}, {}
    cnt = 0
    for line in f:
        if line.startswith('#') or line.strip() == '':  # comment line
            continue
        src, typ, tgt = line.strip().split('\t')
        if decode_unicode(src) in vocabs and decode_unicode(src) not in d:
            d[decode_unicode(src)] = cnt
            d_r[cnt] = decode_unicode(src)
            cnt += 1
        for dec in tgt.split():
            if decode_unicode(dec) in vocabs and decode_unicode(dec) not in d:
                d[decode_unicode(dec)] = cnt
                d_r[cnt] = decode_unicode(dec)
                cnt += 1
    return d, d_r, cnt


def unihan_to_conn(char_id,
                   replace_type='kSemanticVariant&kSimplifiedVariant&kTraditionalVariant&kZVariant',
                   file_path='./Unihan_Variants.txt'):
    replace_types = replace_type.strip().split('&')
    f = open(file_path)
    l = []

    for line in f:
        if line.startswith('#') or line.strip() == '':  # comment line
            continue
        src, typ, tgt = line.strip().split('\t')
        if typ not in replace_types:
            continue
        if decode_unicode(src) not in char_id:
            continue
        src_id = char_id[decode_unicode(src)]
        for dec in tgt.split():
            if decode_unicode(dec) not in char_id:
                continue
            dec_id = char_id[decode_unicode(dec)]
            l.append((dec_id, src_id))
    return l


def get_convert_dict(replace_type, file_path='./Unihan_Variants.txt'):
    replace_type = replace_type.strip()
    f = open(file_path)
    d = {}

    # compositional dict
    if '_' in replace_type:
        type_1, type_2 = replace_type.split('_')
        d_1 = get_convert_dict(type_1, file_path)
        d_2 = get_convert_dict(type_2, file_path)
        for k, v in d_1.items():
            if v in d_2:
                d[k] = d_2[v]
        return dict(d, **d_2)

    for line in f:
        if line.startswith('#') or line.strip() == '':  # comment line
            continue
        src, typ, tgt = line.strip().split('\t')
        if typ == replace_type:
            src_ch = decode_unicode(src)
            tgt_ch = decode_unicode(tgt)
            d[src_ch] = tgt_ch
    return d


def find(data, i):
    if i != data[i]:
        data[i] = find(data, data[i])
    return data[i]


def union(data, i, j):
    pi, pj = find(data, i), find(data, j)
    if pi != pj:
        data[pi] = pj


def connected(data, i, j):
    return find(data, i) == find(data, j)


def get_char_union_id(file_path='./Unihan_Variants.txt'):
    d, d_r, n = char_to_id()
    d_resort = {}
    d_result = {}
    conn = unihan_to_conn(d)
    data = [i for i in range(n)]

    # union
    for i, j in conn:
        union(data, i, j)
    # find
    cnt = 0
    for i in range(n):
        found = find(data, i)
        if found not in d_resort:
            d_resort[found] = cnt
            cnt += 1
        # if need id
        d_result[d_r[i]] = d_resort[found]
        # if need substituted char
        # d_result[d_r[i]] = d_r[found]
    return d_result, cnt


def check_if_all_chars_in_vocab(char_union_id):
    l = get_vocabs()
    for key in char_union_id:
        assert key in l


if __name__ == '__main__':
    char_union_id, cnt = get_char_union_id()
    check_if_all_chars_in_vocab(char_union_id, '/path/to/vocab')
    print(cnt, char_union_id)
