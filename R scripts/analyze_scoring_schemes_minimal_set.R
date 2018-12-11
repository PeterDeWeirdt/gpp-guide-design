library(ggplot2)
library(reshape2)
library(dplyr)
library(pheatmap)
library(RColorBrewer)
library(tidyr)
library(ggpubr)
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
my_RS2 = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-96ad3376.csv')
RS2.Physio = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-3c835d8f.csv')
RS2.OOF = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-a65c930f.csv')
RS2.OOF.Physio = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-c77e9aca.csv')
RS2.OOF.Physio.Zip = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-0c1b08a7.csv')
RS2.OOF.Physio.Zip.Repeat = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-51fe0875.csv')
RS3.Cut.80 = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-6f868758.csv')
RS3.Cut.20.80 = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-00ce2433.csv')
RS3.Cut.100 = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-b0d59069.csv')
RS3.Cut.20.80.pval = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-5471b86c.csv')
RS3.Cut.20.pval.80 = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-c6f6c303.csv')
Cut.80.OOF = read.csv('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/predictions/PredictModel-8cc8ace3.csv')

gecko_V2_filtered = gecko_V2_essential %>%
  filter(sgRNA.context.sequence != '') %>%
  inner_join(predictions, by = 'sgRNA.context.sequence') %>%
  mutate(X30mer = substr(sgRNA.context.sequence, 1, 30)) %>%
  inner_join(my_RS2 %>% select(kmer, predicted) %>%
               dplyr::rename(my.RS2 = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(RS2.Physio %>% select(kmer, predicted) %>%
               dplyr::rename(RS2.Physio = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(RS2.OOF %>% select(kmer, predicted) %>%
               dplyr::rename(RS2.OOF = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(RS2.OOF.Physio %>% select(kmer, predicted) %>%
               dplyr::rename(RS2.OOF.Physio = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(RS2.OOF.Physio.Zip %>% select(kmer, predicted) %>%
               dplyr::rename(RS2.OOF.Physio.Zip = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(RS2.OOF.Physio.Zip.Repeat %>% select(kmer, predicted) %>%
               dplyr::rename(RS2.OOF.Physio.Zip.Repeat = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(RS3.Cut.80 %>% select(kmer, predicted) %>%
               dplyr::rename(RS3.Cut.80 = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(RS3.Cut.20.80 %>% select(kmer, predicted) %>%
               dplyr::rename(RS3.Cut.20.80 = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(RS3.Cut.100 %>% select(kmer, predicted) %>%
               dplyr::rename(RS3.Cut.100 = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(Cut.80.OOF %>% select(kmer, predicted) %>%
               dplyr::rename(Cut.80.OOF = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(RS3.Cut.20.80.pval %>% select(kmer, predicted) %>%
               dplyr::rename(RS3.Cut.20.80.pval = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  inner_join(RS3.Cut.20.pval.80 %>% select(kmer, predicted) %>%
               dplyr::rename(RS3.Cut.20.pval.80 = predicted, X30mer = kmer), by = 'X30mer') %>%
  distinct() %>%
  rename(Rule.Set.1 = doench)
  
  
scoring_schemes = c('Rule.Set.2', 'CRISPRater', 'TUSCAN', 'predictSGRNA', 'Xu', 
                    'crisprScan', 'Rule.Set.1', 'Housden', 'Chari', 'WU.CRISPR', 'Wang', 'my.RS2', 'RS2.Physio', 
                    'RS2.OOF', 'RS2.OOF.Physio', 'RS2.OOF.Physio.Zip',
                    'RS2.OOF.Physio.Zip.Repeat', 'RS3.Cut.80', 'RS3.Cut.20.80', 
                    'RS3.Cut.100', 'Cut.80.OOF', 'RS3.Cut.20.80.pval', 'RS3.Cut.20.pval.80')
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
## RS2
models = c('Rule.Set.2', 'CRISPRater', 'TUSCAN', 'predictSGRNA', 'Xu', 
           'crisprScan', 'Rule.Set.1', 'Housden', 'Chari', 'WU.CRISPR', 'Wang', 'my.RS2')
ggplot(cell_score_cor %>% filter(Scoring_Scheme %in% models)) +
  aes(x=Scoring_Scheme, y = Correlation, fill = Scoring_Scheme) +
  geom_boxplot() +
  theme_classic() +
  theme(legend.position = '', axis.text.x = element_text(angle=45, hjust = 1), 
        text = element_text(size=16), axis.text = element_text(color = 'black')) +
  geom_hline(yintercept = cell_score_cor %>% filter(Scoring_Scheme == 'Rule.Set.2') %>% 
               select(Correlation) %>% unlist() %>% median(), linetype = 'dashed') +
  xlab('Scoring Scheme') +
  scale_fill_brewer(palette = 'Set3') 
  ggsave('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/presentations/RD_12-5-18/perf_rs2.pdf')
## Features
ggplot(cell_score_cor %>% filter(Scoring_Scheme %in% c('Rule.Set.2', 'predictSGRNA', 'Rule.Set.1', 'RS2.Physio', 
                                                       'RS2.OOF', 'RS2.OOF.Physio', 'RS2.OOF.Physio.Zip', 
                                                       'RS2.OOF.Physio.Zip.Repeat'))) +
  aes(x=Scoring_Scheme, y = Correlation, fill = Scoring_Scheme) +
  geom_boxplot() +
  theme_classic() +
  theme(legend.position = '', axis.text.x = element_text(angle=45, hjust = 1), 
        text = element_text(size=16), axis.text = element_text(color = 'black')) +
  geom_hline(yintercept = cell_score_cor %>% filter(Scoring_Scheme == 'Rule.Set.2') %>% 
               select(Correlation) %>% unlist() %>% median(), linetype = 'dashed') +
  xlab('Scoring Scheme') +
  scale_fill_brewer(palette = 'Set3')
  ggsave('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/presentations/RD_12-5-18/perf_feats.pdf')
## New Filtering
ggplot(cell_score_cor %>% filter(Scoring_Scheme %in% c('Rule.Set.2', 'predictSGRNA', 'Rule.Set.1', 
                                                       'RS2.OOF.Physio.Zip.Repeat', 'RS3.Cut.80', 'RS3.Cut.20.80', 
                                                       'RS3.Cut.100', 'RS3.Cut.20.80.pval', 'Cut.80.OOF'))) +
  aes(x=Scoring_Scheme, y = Correlation, fill = Scoring_Scheme) +
  geom_boxplot() +
  theme_classic() +
  theme(legend.position = '', axis.text.x = element_text(angle=60, hjust = 1),
        axis.text = element_text(color = 'black'),
        text = element_text(size=16)) +
  geom_hline(yintercept = cell_score_cor %>% filter(Scoring_Scheme == 'Rule.Set.2') %>% 
               select(Correlation) %>% unlist() %>% median(), linetype = 'dashed') +
  xlab('Scoring Scheme') +
  scale_fill_brewer(palette = 'Set3')
  ggsave('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/presentations/RD_12-5-18/filt.pdf')

## p-values
ggboxplot(cell_score_cor %>% filter(Scoring_Scheme %in% c('Rule.Set.2', 'Rule.Set.1', 'RS3.Cut.20.80.pval', 'predictSGRNA')), 
          x='Scoring_Scheme', y='Correlation', fill = 'Scoring_Scheme') +
  stat_compare_means(comparisons = list(c('Rule.Set.2', 'Rule.Set.1'), c('predictSGRNA', 'Rule.Set.2'), 
                                        c('Rule.Set.2', 'RS3.Cut.20.80.pval')), 
                     method = 't.test', size = 5) +
  theme( text = element_text(size=16), axis.text.x = element_text(angle=45, hjust = 1)) +
  xlab('Scoring Scheme') +
  scale_fill_brewer(palette = 'Set3') +
  labs(fill = '')
  ggsave('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/presentations/RD_12-5-18/pvals.pdf')


melted_gecko = gecko_V2_filtered %>%
  group_by(Ensembl.Gene.ID, Cell.Type) %>%
  mutate(true_rank = factor(rank(-sgRNA.measured.value, ties.method = 'max'))) %>%
  mutate(Rule.Set.1.rank = rank(-Rule.Set.1, ties.method = 'max')) %>%
  mutate(predictSGRNA.rank = rank(-predictSGRNA, ties.method = 'max')) %>%
  mutate(Rule.Set.2.rank = rank(-Rule.Set.2, ties.method = 'max')) %>%
  mutate(RS3.Cut.20.80.pval.rank = rank(-RS3.Cut.20.80.pval, ties.method = 'max')) %>%
  ungroup() %>%
  select(sgRNA.Sequence, Cell.Type, Ensembl.Gene.ID, 
         true_rank, Rule.Set.1.rank, predictSGRNA.rank, Rule.Set.2.rank, RS3.Cut.20.80.pval.rank) %>%
  melt(id.vars = c('sgRNA.Sequence', 'Cell.Type', 'Ensembl.Gene.ID', 'true_rank'))
Avg_rank = melted_gecko %>%
  group_by(Cell.Type, true_rank, variable) %>%
  summarise(Avg.Rank = mean(value)) %>%
  ungroup()
  
  
  

ggboxplot(Avg_rank %>% filter(true_rank %in% factor(c(1,2,3,4,5,6))),
          x='true_rank', y='Avg.Rank', fill = 'variable') +
  scale_fill_brewer(palette = 'Set3') +
  labs(fill = '') +
  xlab('Avg. Rank') +
  ylab('True Rank')

delta_rank = Avg_rank %>%
  dcast(Cell.Type + variable ~  true_rank, value.var = 'Avg.Rank') %>%
  group_by(Cell.Type, variable) %>%
  mutate(delta.6.1 = `6` - `1`)

ggboxplot(delta_rank, x='variable', y='delta.6.1', fill = 'variable') +
  scale_fill_brewer(palette = 'Set3') +
  stat_compare_means(comparisons = list(c('Rule.Set.1.rank', 'Rule.Set.2.rank'), 
                                        c('predictSGRNA.rank', 'Rule.Set.2.rank'),
                                        c('RS3.Cut.20.80.pval.rank', 'Rule.Set.2.rank'))) +
  ylab('Avg. Rank Guide 6 - Avg. Rank Guide 1') +
  xlab('') +
  labs(fill = '') +
  theme(axis.text.x = element_text(angle = 45,  hjust = 1))
ggsave('/Users/pdeweird/Documents/csci-e-29/final_project-PeterDeWeirdt/data/presentations/RD_12-5-18/rank-diff-pvals.pdf')

