# -1 - Detected Correctly
# 0 - Not Detected
# 1 - Detected too much characters
# 2 - Detected too few  character
def format_license_plate(lps):
    print(lps)
    lps = [s.replace(" ", "") for s in lps]
    lps = [s.replace(":", "") for s in lps]
    lps = [s.replace("~", "") for s in lps]
    lps = [s.replace("/", "") for s in lps]
    lps = [s.replace("?", "") for s in lps]
    lps = [s.replace("_", "") for s in lps]
    lps = [s.replace("-", "") for s in lps]

    if len(lps) == 0:
        return (0, "")
    if len(lps) == 1:
        lp = lps[0]
        if len(lp) > 8:
            return (1, "")
        if(len(lp)) < 4:
            return (2, "")
        return -1, lps[0]
    lps = [s for s in lps if s != "PL"]  # Delete "PL" if reader cach this
    lps = [s for s in lps if len(s) < 7] # Delete not part of LP
    if len(lps) > 2:
        return (1, "")
    
    lps_sort = sorted(lps, key=len)
    lp = "".join(lps_sort)
    if  len(lp) < 3 or len(lp) > 8:
        return 1, ""
    print("DETECTED")
    print(lp)
    return -1, "".join(lps_sort)

    