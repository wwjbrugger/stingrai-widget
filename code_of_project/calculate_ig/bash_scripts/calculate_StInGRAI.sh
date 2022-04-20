# start script with bash calculate_StInGRAI.sh
#!/bin/bash
# path to the virtual environment you would like to use
source ~/PycharmProjects/stingrai-widget/venv/bin/activate
# path to the root of the project
export PYTHONPATH=$PYTHONPATH:~/PycharmProjects/stingrai-widget/
#path to the start_integrated_gradient.py folder
cd ~/PycharmProjects/stingrai-widget/code_of_project/calculate_ig
#name of the folders you would like to analyze
# navigate in terminal to folder with ls -a all fills are shown copy them and insert below
folder_to_analyze=(
   '0.0-0.1->0.1-0.2.pkl'  '0.2-0.3->0.2-0.3.pkl'  '0.3-0.4->0.4-0.5.pkl'  '0.5-0.6->0.5-0.6.pkl'  '0.6-0.7->0.7-0.8.pkl'  '0.8-0.9->0.8-0.9.pkl'             '0.1-0.2->0.1-0.2.pkl'  '0.2-0.3->0.3-0.4.pkl'  '0.4-0.5->0.4-0.5.pkl'  '0.5-0.6->0.6-0.7.pkl'  '0.7-0.8->0.7-0.8.pkl'  '0.8-0.9->0.9-1.0.pkl'
'0.0-0.1->0.0-0.1.pkl'  '0.1-0.2->0.2-0.3.pkl'  '0.3-0.4->0.3-0.4.pkl'  '0.4-0.5->0.5-0.6.pkl'  '0.6-0.7->0.6-0.7.pkl'  '0.7-0.8->0.8-0.9.pkl'
 )
for folder in "${folder_to_analyze[@]}";do
  echo  $folder is analyzed
  python start_integrated_gradient.py --interval_name $folder --folder_name_index StInGRAI
done
