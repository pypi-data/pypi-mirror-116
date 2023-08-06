import sys, os
from ml_deploy.utils import load_class, get_args
sys.path.append(os.getcwd())

args, unknown_args = get_args()


def main():
    interface_name = args.interface_name
    user_class = load_class(interface_name)
    user_model = user_class()
    user_model.api_resources()
    user_model.run()

if __name__ == '__main__':
    main()