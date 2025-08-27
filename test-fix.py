try:
    from allin1.models.dinat import DinatLayer1d, DinatLayer2d
    print("OK: DiNAT importó con shim de NATTEN")
except Exception as e:
    import traceback; traceback.print_exc(); exit(1)

