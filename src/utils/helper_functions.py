def get_env_from_system_args(args):
    for  i in range(len(args)):
        if args[i].lower() == "env":
            return args[i + 1].lower()

    return ""