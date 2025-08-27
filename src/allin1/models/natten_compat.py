try:
    # API 0.17.x
    from natten.functional import natten1dqkrpb as na1d_qk
    from natten.functional import natten1dav    as na1d_av
    from natten.functional import natten2dqkrpb as na2d_qk
    from natten.functional import natten2dav    as na2d_av
except Exception:
    # API >=0.20
    from natten.functional import na1d_qk, na1d_av, na2d_qk, na2d_av
