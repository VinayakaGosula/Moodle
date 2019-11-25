ans=$(bash $1/q1.sh)
echo q1:
if [ $ans -eq 10 ]
then
	echo 100
else
	echo 0
fi
echo 100
echo ''
ans1=$(bash $1/q2.sh)
echo q2:
if [ $ans1 -eq 5 ]
then
	echo 100
else
	echo 0
fi	
echo 100
echo ''
