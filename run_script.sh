stage=$1
if test -z "$stage"
then
  stage="dev"
fi
python3 -m MeatuchuRPGMapMaker --arg "$stage"