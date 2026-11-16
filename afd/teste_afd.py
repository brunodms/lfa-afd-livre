def test_aceitos():
    afd = gerar("entrada.txt")
    for t in ["se", "entao", "senao"]:
        assert aceita(afd, t)

def test_rejeitados():
    afd = gerar("entrada.txt")
    assert not aceita(afd, "s")
    assert not aceita(afd, "xyz")