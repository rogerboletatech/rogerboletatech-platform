import re

from boleta.ulid import gerar_ulid


def test_ulid_tem_26_caracteres_crockford():
    assert re.fullmatch(r"[0-9A-HJKMNP-TV-Z]{26}", gerar_ulid())


def test_ulids_sao_unicos():
    assert len({gerar_ulid() for _ in range(1000)}) == 1000


def test_ulid_ordena_no_tempo():
    primeiro = gerar_ulid()
    segundo = gerar_ulid()
    assert primeiro[:10] <= segundo[:10]
