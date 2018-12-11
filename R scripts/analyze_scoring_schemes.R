library(ggplot2)
library(reshape2)
library(dplyr)
library(pheatmap)
gecko_V2 = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/ddAUC/GeCKOv2_essential_nonessential_v4.csv')
predictions = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/ddAUC/Gv2_all_scores.txt', sep='\t',
                         header = TRUE)
gecko_V2_essential = gecko_V2 %>% filter(Essential.genes == 'Y') 
gecko_cell_correlation = gecko_V2_essential %>%
  mutate(Cell_Context = paste(sgRNA.context.sequence, Cell.Type)) %>%
  select(Cell_Context, sgRNA.context.sequence, Cell.Type, sgRNA.measured.value) %>%
  reshape2::dcast(sgRNA.context.sequence~Cell.Type, value.var = 'sgRNA.measured.value', fun = sum) %>%
  filter(sgRNA.context.sequence != '') %>%
  select(-sgRNA.context.sequence) %>%
  cor()
pheatmap(gecko_cell_correlation)  
mean_cell_correlation = melt(gecko_cell_correlation) %>%
  group_by(Var1) %>%
  dplyr::summarise(mean_cor = mean(value))
# Use the most well correlated Cell.Line as our test set, but we
# will bring back to test every cell line
top_cell = mean_cell_correlation %>% top_n(1, mean_cor) %>%
  select(Var1)
dimer = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-b17e9960.csv')
my_rs2 = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-96ad3376.csv')
rs2_physio = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-3c835d8f.csv')
rs2_param = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-9e29b69b.csv')
rs2_OOF = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-a65c930f.csv')
rs2_OOF_physio = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-c77e9aca.csv')
rs2_OOF_physio_zip = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-0c1b08a7.csv')
rs2_OOF_physio_double_zip = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-a400c40d.csv')
rs2_OOF_physio_zip_repeat = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-51fe0875.csv')
rs3_OOF_physio_zip_repeat = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-89e922ef.csv')
rs3_OOF_physio_zip_repeat_cd3e = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-2629cc11.csv')
rs3_OOF_physio_zip_repeat_cd28 = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-d8e94b66.csv')
rs3_OOF_physio_zip_repeat_MED12 = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-25330b53.csv')
rs3_OOF_physio_zip_repeat_90 = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-4f0260ec.csv')

gecko_V2_filtered = gecko_V2_essential %>%
  filter(sgRNA.context.sequence != '') %>%
  inner_join(predictions, by = 'sgRNA.context.sequence') %>%
  mutate(X30mer = substr(sgRNA.context.sequence, 1, 30)) %>%
  inner_join(my_rs2 %>% select(kmer, predicted) %>%
               dplyr::rename(myRS2 = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(dimer %>% select(kmer, predicted) %>%
               dplyr::rename(dimer = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs2_physio %>% select(kmer, predicted) %>%
               dplyr::rename(rs2_physio = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs2_param %>% select(kmer, predicted) %>%
               dplyr::rename(rs2_param = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs2_OOF %>% select(kmer, predicted) %>%
               dplyr::rename(rs2_OOF = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs2_OOF_physio %>% select(kmer, predicted) %>%
               dplyr::rename(rs2_OOF_physio = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs2_OOF_physio_zip %>% select(kmer, predicted) %>%
               dplyr::rename(rs2_OOF_physio_zip = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs2_OOF_physio_double_zip %>% select(kmer, predicted) %>%
               dplyr::rename(rs2_OOF_physio_double_zip = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs2_OOF_physio_zip_repeat %>% select(kmer, predicted) %>%
               dplyr::rename(rs2_OOF_physio_zip_repeat = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs3_OOF_physio_zip_repeat %>% select(kmer, predicted) %>%
               dplyr::rename(rs3_OOF_physio_zip_repeat = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs3_OOF_physio_zip_repeat_cd3e %>% select(kmer, predicted) %>%
               dplyr::rename(rs3_OOF_physio_zip_repeat_cd3e = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs3_OOF_physio_zip_repeat_cd28 %>% select(kmer, predicted) %>%
               dplyr::rename(rs3_OOF_physio_zip_repeat_cd28 = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs3_OOF_physio_zip_repeat_CUL3 %>% select(kmer, predicted) %>%
               dplyr::rename(rs3_OOF_physio_zip_repeat_CUL3 = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs3_OOF_physio_zip_repeat_MED12 %>% select(kmer, predicted) %>%
               dplyr::rename(rs3_OOF_physio_zip_repeat_MED12 = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(rs3_OOF_physio_zip_repeat_90 %>% select(kmer, predicted) %>%
               dplyr::rename(rs3_OOF_physio_zip_repeat_90 = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct()
  
scoring_schemes = c('Rule.Set.2', 'CRISPRater', 'TUSCAN', 'predictSGRNA', 'Xu', 
                    'crisprScan', 'doench', 'Housden', 'Chari', 'WU.CRISPR', 'Wang', 'myRS2', 'rs2_physio', 
                    'rs2_OOF', 'dimer', 'rs2_OOF_physio', 'rs2_param', 'rs2_OOF_physio_zip', 'rs2_OOF_physio_double_zip',
                    'rs2_OOF_physio_zip_repeat', 'rs3_OOF_physio_zip_repeat', 'rs3_OOF_physio_zip_repeat_cd3e',
                    'rs3_OOF_physio_zip_repeat_cd28', 'rs3_OOF_physio_zip_repeat_CUL3', 'rs3_OOF_physio_zip_repeat_MED12', 
                    'rs3_OOF_physio_zip_repeat_90')
cell_score_cor = data.frame(Cell = rep(NA, length(unique(gecko_V2_essential$Cell.Type))*
                                         length(scoring_schemes)),
                            Correlation = rep(NA, length(unique(gecko_V2_essential$Cell.Type))*
                                                length(scoring_schemes)),
                            Scoring_Scheme = rep(NA, length(unique(gecko_V2_essential$Cell.Type))*
                                                   length(scoring_schemes))
                            )
i = 1
for (cell in unique(gecko_V2_essential$Cell.Type)) {
  print(i)
  scores_acitvity_cor = gecko_V2_filtered %>%filter(Cell.Type == cell) %>% 
    select(unlist(c('sgRNA.measured.value', scoring_schemes))) %>%
    cor(method= 'spearman')
  curr_scores = scores_acitvity_cor[1, -1]
  cell_score_cor[i:(i+length(curr_scores) - 1), 'Cell'] = rep(cell, length(curr_scores))
  cell_score_cor[i:(i+length(curr_scores) - 1), 'Correlation'] = curr_scores
  cell_score_cor[i:(i+length(curr_scores) - 1), 'Scoring_Scheme'] = names(curr_scores)
  i = i + length(curr_scores)
}
best_cor_scheme = cell_score_cor %>%
  group_by(Scoring_Scheme) %>%
  dplyr::summarise(median_cor = median(Correlation)) %>%
  arrange(median_cor) %>%
  select(Scoring_Scheme)
cell_score_cor['Scoring_Scheme'] = factor(cell_score_cor$Scoring_Scheme, 
                                          levels = best_cor_scheme$Scoring_Scheme)
ggplot(cell_score_cor) +
  aes(x=Scoring_Scheme, y = Correlation, fill = Scoring_Scheme) +
  theme(legend.position = '', axis.text.x = element_text(angle=45, hjust = 1)) +
  geom_boxplot()

t.test(cell_score_cor %>% filter(Scoring_Scheme == 'Rule.Set.2') %>% select('Correlation'), cell_score_cor %>% filter(Scoring_Scheme == 'rs3_OOF_physio_zip_repeat_90') %>% select('Correlation'))
write.csv(gecko_V2_filtered %>% filter(Cell.Type == top_cell[[1]]), 
          paste('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/raw/', 
                as.character(top_cell[[1]]), '_essential.csv', sep=''))


