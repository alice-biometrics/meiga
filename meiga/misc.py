def get_args_list(args):
    list_args = args
    if isinstance(args, tuple):
        list_args = list(args)
    else:
        if not isinstance(args, list):
            list_args = [args]
    return list_args
