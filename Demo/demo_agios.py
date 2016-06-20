import corna
from corna import config

config.NAME_COL = 'Name'
# path to directory where multiquant text data files are present
path_dir = '/Users/sininagpal/OneDrive/Elucidata_Sini/NA_correction/Demo/data_agios/'

# read maven data
#single tracer data
#maven_data = corna.read_maven(path_dir + '/data_single_tracer_std.csv')
maven_data = corna.read_maven(path_dir + '/aceticacid.csv')

# multiple tracer data
#maven_data = corna.read_maven(path_dir + '/data_multiple_tracers_std.csv')
#std_input_data = corna.convert_inputdata_to_stdfrom(maven_data)

# For json input, use this funtion:
#json_input = json.dumps(maven_data.to_dict())
#maven_data = corna.convert_json_to_df(json_input)

# read maven metadata file
maven_metadata = corna.read_mvn_metadata(path_dir + '/metadata.csv')

# merge maven files and metadata files
merge_mv_metdata = corna.merge_mvn_metadata(maven_data, maven_metadata)

# tracer isotopes
iso_tracers = ['C13']
#iso_tracers = ['C13', 'N15']

#element to be corrected
eleme_corr = {'C': ['H', 'O'], 'N': ['S']}
#eleme_corr = {}

# NA values dict
na_dict = corna.get_na_dict(iso_tracers, eleme_corr)
na_dict = {'H': [0.99, 0.00015], 'C': [0.99, 0.011], 'S': [0.922297, 0.046832, 0.030872], 'O': [0.99757, 0.00038, 0.00205], 'N': [0.99636, 0.00364]}
# edit na values
#na_dict['H'][0] = 0.989

# NA correction single tracer
#na_corr_dict = corna.na_corr_single_tracer_mvn(merge_mv_metdata, iso_tracers, eleme_corr, na_dict, optimization = False)
#na_corr_df = corna.convert_to_df(na_corr_dict, colname = 'NA corrected')
#print na_corr_df

# NA correction multiple tracer
na_corr_dict = corna.na_correction(merge_mv_metdata, iso_tracers, eleme_corr, na_dict, optimization = True)
#na_corr_dict = corna.na_corr_multiple_tracer(merge_mv_metdata, iso_tracers, eleme_corr, na_dict, optimization = True)
na_corr_df = corna.convert_to_df(na_corr_dict, colname = 'NA corrected')
print na_corr_df
# Replace negative values by zero on NA corrected data - optional
postprocessed_out = corna.replace_negatives(na_corr_dict, replace_negative = True)
postprocessed_out_df = corna.convert_to_df(postprocessed_out, colname =  'CorrIntensities-Replaced_negatives')

# calculate fractional enrichment on post processed data
frac_enrichment = corna.fractional_enrichment(postprocessed_out,)
frac_enr_df = corna.convert_to_df(frac_enrichment, colname = 'Frac Enrichment')
print frac_enr_df

# combine results - dataframe with na correction column, frac enrichment column and post processed column
df_list = [na_corr_df, frac_enr_df, postprocessed_out_df, merge_mv_metdata]
merged_results_df = corna.merge_dfs(df_list)

# filter any dataframe as per requirement and save it to csv
# filter by one column - sample name
sample_1_data = corna.filtering_df(frac_enr_df, num_col=1, col1="Sample Name",
                                list_col1_vals=['sample_1'])

# filter by two columns - metabolite name and label
filtered_data = corna.filtering_df(frac_enr_df, num_col=2, col1="Name",
                                list_col1_vals=['L-Methionine'], col2="Sample Name", list_col2_vals=['sample_1', 'sample_2'])


filtered_data = corna.filtering_df(frac_enr_df, num_col=3, col1="Name",
                                list_col1_vals=['L-Methionine'], col2="Sample Name", list_col2_vals=['sample_1', 'sample_2'],\
                                col3="Label", list_col3_vals = ['C13_1_N15_0', 'C13_2_N15_0'])

# save any dataframe at given path
#save_dfs = corna.save_to_csv(merged_results_df, path_dir + 'results.csv')

