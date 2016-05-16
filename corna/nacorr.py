import os
import sys

import helpers as hl
import file_parser as fp
import isotopomer as iso
import preprocess as preproc
import postprocess as postpro


# setting relative path
basepath = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(basepath, "..", "data"))


# Maven

# read files
input_data = hl.read_file(data_dir + '/maven_output.csv')
metadata = hl.read_file(data_dir + '/metadata.csv')

# merge data file and metadata
merged_df = fp.maven_merge_dfs(input_data, metadata)

# filter df if reqd , given example
filter_df = hl.filter_df(merged_df, 'Sample Name', 'sample_1')

# std model maven
std_model_mvn = fp.standard_model(merged_df, parent = False)



# MultiQuant

# read files
mq_df = hl.concat_txts_into_df(data_dir + '/')
mq_metdata = hl.read_file(data_dir + '/mq_metadata.xlsx')

# merge mq_data + metadata
merged_data = fp.mq_merge_dfs(mq_df, mq_metdata)
merged_data.to_csv(data_dir + '/merged_mq.csv')

# standard model mq
std_model_mq = fp.standard_model(merged_data, parent = True)

# Pyruvate 87/87 - C3H3O3/C3H3O3
# Lactate 89/89 - C3H5O3/C3H5O3
# Citrate 191/67 - C6H7O7/C4H3O
# Citrate 191/111 - C6H7O7/C5H3O3
# Glutamate 146/128 - C5H8NO4/C5H6NO3
# Glutamate 146/41 - C5H8NO4/C2H4O
# Succinate 117/99 - C4H5O4/C4H3O3
# Succinate 117/73 - C4H5O4/C3H5O2
# Malate 133/115 - C4H5O5/C4H3O4
# PEP 167/79 - C3H4O6P/O3P
# Taurine 124/80 - C2H6NO3S/O3S

# integrating isotopomer and parser (input is standardised model in form of nested dictionaries)
fragments_dict = {}
for frag_name, label_dict in std_model_mq.iteritems():
    if frag_name[2] == 'Glutamate 146/41':
        new_frag_name = (frag_name[0], frag_name[1], frag_name[3])
        fragments_dict.update(iso.bulk_insert_data_to_fragment(new_frag_name, label_dict, mass=True, number=False, mode=None))

print fragments_dict

# preprocessing : correction for background noise
preprocess_data = preproc.background('A. [13C-glc] G2.5 0min', fragments_dict[('Glutamate 147/41_147.0', 'Glutamate 147/41_41.0')],\
 fragments_dict[('Glutamate 146/41_146.0', 'Glutamate 146/41_41.0')])


# na correction
#code from algorithm.py

# post processing - replace negative values by zero
# tested on std_model_mvn and std_model_mq - same data format as output from algorithm.py
#post_processed_dict = postpro.replace_negative_to_zero(std_model_mvn, replace_negative = True)
#print post_processed_dict


# output: convert nested dictionary to pandas data frame and add columns from merged df
















