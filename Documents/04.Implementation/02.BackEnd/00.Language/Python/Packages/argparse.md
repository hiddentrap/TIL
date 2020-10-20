# Argparse (파라메터 파서)

```python
def get_args():
    """parameter parser"""
    
    parser = argparse.ArgumentParser(
        description = '프로그램 설명',
        formatter_class = argparse.ArgumentDefaultHelpFormatter)
    
    parser.add_argument('positional', # 이름, -가 없어서 위치 파라메터로 인식
                       metavar='str, # 데이터 타입 힌트, 기본값은 string
                        help='A positional argument') # 파라메터 설명
    # nargs=2 값 갯수 제한(2), '+' 1이상 return list
    
    parser.add_argument('file2',
                       metavar='str',
                       type=str,
                       help='Input file')
    
    parser.add_argument('-a', # 짧은이름
                       '--arg', # 김이름
                       help='A named string argument',
                       metavar='str', # 데이터 타입 힌트
                       type=str, # 실제 데이터 타입
                       default='') # 기본값
    # 필수값으로 지정하고 싶으면 default 없애고, required=True 부여
    # choices=['red','yellow','blue'] 값 제한
    
    parser.add_argument('-i',
                       '--int',
                       help='A named integer argument',
                       metavar='int',
                       type=int,
                       default=0)
    # choices = range(1,11) 값 제한
    
    parser.add_argument('-f',
                       '--file',
                       help='A readable file',
                       metavar='FILE',
                       type=argparse.FileType('rt', encodings='UTF8'),
                       default=None)
    # 파일 유효성 체크 알아서 해줌 return 파일 핸들러
    
    parser.add_argument('-o',
                       '--on',
                       help='A boolean flag',
                       action='store_true') # 플래그 기술시 True, 기본은 False
    
    args = parser.parse_args()
    
    # 파일을 string으로 받을경우 체크해서 핸들러 가져와야함
    if not os.path.isfile(args.file2):
        parser.error(f'"{args.file2}" is not a file)
    args.file2 = open(args.file2)
    
   if not 1 <= args.val <=10:
        parser.error(f'--val "{args.val}" must be between 1 and 10')
                     
    return args

#--------------------------------------------------------------

def main():
    """Main"""
    args = get_args()
    int_arg = args.int
```

