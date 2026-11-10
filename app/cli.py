import argparse, json
from .pipeline import SafeRAG
def main():
    parser=argparse.ArgumentParser(description="Indirect prompt injection detection demo")
    parser.add_argument("--question",required=True)
    args=parser.parse_args()
    print(json.dumps(SafeRAG().answer(args.question),indent=2))
if __name__=="__main__": main()
