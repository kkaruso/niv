import yaml
from arg_parser import ArgParser

arg_parser = ArgParser()
args = ArgParser.get_args()

# if __name__ == '__main__':
# if args.convert is not None:
#     file_name = str(args.convert).split('\\')[-1]  # get filename
#     print(file_name)
#     with open(file_name, 'r') as stream:
#         try:
#             print(yaml.safe_load(stream))
#         except yaml.YAMLError as exc:
#             print(exc)
