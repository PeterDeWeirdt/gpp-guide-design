Gv2_OOF = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/raw/OOF_Mutation_Rates_Gv2.csv') %>%
  select(guide, OOF.Mutation.Rate)
Gv2_EWS502 = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/raw/EWS502_BONE_essential.csv')
Gv2_EWS502_OOF = inner_join(Gv2_OOF, Gv2_EWS502, by=c('guide' = 'sgRNA.Sequence')) %>%
  distinct()
write.csv(Gv2_EWS502_OOF, '/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/raw/Gv2_TEST_V1.csv')
