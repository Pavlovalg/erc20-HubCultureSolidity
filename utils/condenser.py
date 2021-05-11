if __name__ == "__main__":
    with open('../contracts/HubCulture.sol') as f:
        source_token = f.readlines()

    with open('../contracts/SafeMath.sol') as f:
        source_math = f.readlines()

    with open('../contracts/ERC20Lib.sol') as f:
        source_erc = f.readlines()

    pragma = source_token[0]

    source_erc = source_erc[3:]
    source_math = source_math[1:]
    source_token = source_token[3:]

    with open("condensed.sol",'w') as f:
        f.write(pragma)
        for line in source_math:
            f.write(line)
        for line in source_erc:
            f.write(line)
        for line in source_token:
            f.write(line)
