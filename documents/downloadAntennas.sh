
echo "going to Documents folder"
cd /tmp/
echo "removing old files"
rm radiation_non_ionizing_active_cellular_antennas.xlsx
echo "downloading new file"
/usr/bin/wget https://data.gov.il/dataset/995eb826-c471-4572-8fd3-39d92a3a9603/resource/8935c8e5-ec77-421f-af86-d970583195f8/download/radiation_non_ionizing_active_cellular_antennas.xlsx
ls -lart

