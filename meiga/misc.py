def get_args_list(args):
    if isinstance(args, tuple):
        list_args = list(args)
    else:
        list_args = [args]
    return list_args
