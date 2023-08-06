from yalm import licenses

mit, apache, *_ = list(licenses.spdx_licenses.values())

template = apache
key = '9409774ee89c484fe0f4b65d12bda1d2923d4687686858679172d473cd83038c.txt'

doc = licenses._normalize_text(template.positive_sample(key).document)
pattern = apache.regex.pattern
