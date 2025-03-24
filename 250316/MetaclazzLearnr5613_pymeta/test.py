from newdig.stdauth import digesters
# from newdig.stdauth import SHA256
# from newdig.stdauth import SHA256 # type: ignore

if __name__ == "__main__":
    from_dict = True
    # digesterClazz = digesters["sha256"] if from_dict else SHA256
    digesterClazz = digesters["sha256"]

    print(digesters)

    # print(f"Class name: {digesterClazz.__name__}")
    # print(f"Alg name: {digesterClazz.name}")
    # print(f"Alg digest size: {digesterClazz.digest_size}")
    # digester = digesterClazz()
    # data = b"data"
    # data_digested = digester.digest(data)
    # print(f"Data digest hex: {data_digested.hex()}")

