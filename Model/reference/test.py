from _hangul import normalize

str = "한글테스트 123 abc.....!@#!@$%RT#RG asd ㅅ,ㅎ<ㅁㄴ?>"
print(normalize(str,english=True,number=True,punctuation=True))
