### not run
### this script is only for me to check something

### add soft link
ln -s ../../db/annovar ./annovar # link to in-house db
rm -rf annovar

### note
# if input have NaN in the int column, the output of the int col will be float col. 