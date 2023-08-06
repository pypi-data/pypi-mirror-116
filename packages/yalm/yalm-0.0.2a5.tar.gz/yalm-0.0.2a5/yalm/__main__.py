from yalm import licenses

mit, apache, gpl2, gpl3, *_ = list(licenses.spdx_licenses.values())

template = gpl3
key = '9409774ee89c484fe0f4b65d12bda1d2923d4687686858679172d473cd83038c.txt'
key = 'c65379247414a47f9353192b1e85bbcccb2b703ee3f0df95e0d7eb682035f09d.txt'

raw_doc = template.positive_sample(key).document
doc = licenses._normalize_text(raw_doc)
pattern = apache.regex.pattern
