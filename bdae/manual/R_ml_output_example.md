### R 분석 출력 예제

분석 공부를 하면서, AI 알고리즘을 적용하고 중간단계의 출력들(차트, 모델, ..) <br>
을 모두 한번에 출력하려면 ? 하는 고민을 했었음.

```
library(MASS)
library(dplyr)
library(tidyr)
library(ggplot2)
library(ggplot2)
library(jpeg)
library(lubridate)
library(splines)
library(mgcv)

lung <- read.csv('C:/Users/Admin/Downloads/LungDisease.csv')
house <- read.csv('C:/Users/Admin/Downloads/house_sales.csv', sep='\t')

model <- lm(PEFR ~ Exposure, data=lung)

house_lm <- lm(AdjSalePrice ~ SqFtTotLiving + SqFtLot + Bathrooms + 
                 Bedrooms + BldgGrade,  
               data=house, na.action=na.omit)
			   
house_full <- lm(AdjSalePrice ~ SqFtTotLiving + SqFtLot + Bathrooms + 
                   Bedrooms + BldgGrade + PropertyType + NbrLivingUnits + 
                   SqFtFinBasement + YrBuilt + YrRenovated + NewConstruction,
                 data=house, na.action=na.omit)
				 
step_lm <- stepAIC(house_full, direction="both")				 

house$Year = year(house$DocumentDate)
house$Weight = house$Year - 2005

house_wt <- lm(AdjSalePrice ~ SqFtTotLiving + SqFtLot + Bathrooms + 
                 Bedrooms + BldgGrade,
               data=house, weight=Weight, na.action=na.omit)
round(cbind(house_lm=house_lm$coefficients,house_wt=house_wt$coefficients), digits=3)

zip_groups <- house %>%
  mutate(resid = residuals(house_lm)) %>%
  group_by(ZipCode) %>%
  summarize(med_resid = median(resid),
            cnt = n()) %>%
  # sort the zip codes by the median residual
  arrange(med_resid) %>%
  mutate(cum_cnt = cumsum(cnt),
         ZipGroup = factor(ntile(cum_cnt, 5)))
house <- house %>%
  left_join(dplyr::select(zip_groups, ZipCode, ZipGroup), by='ZipCode')
  
update(step_lm, . ~ . -SqFtTotLiving - SqFtFinBasement - Bathrooms)

house_98105 <- house[house$ZipCode == 98105,]
lm_98105 <- lm(AdjSalePrice ~ SqFtTotLiving + SqFtLot + Bathrooms + 
                 Bedrooms + BldgGrade, data=house_98105)

sresid <- rstandard(lm_98105)
idx <- order(sresid, decreasing=FALSE)
sresid[idx[1]]
resid(lm_98105)[idx[1]]

std_resid <- rstandard(lm_98105)
cooks_D <- cooks.distance(lm_98105)
hat_values <- hatvalues(lm_98105)
plot(subset(hat_values, cooks_D > 0.08), subset(std_resid, cooks_D > 0.08), 
     xlab='hat_values', ylab='std_resid',
     cex=10*sqrt(subset(cooks_D, cooks_D > 0.08)), pch=16, col='lightgrey')
points(hat_values, std_resid, cex=10*sqrt(cooks_D))
abline(h=c(-2.5, 2.5), lty=2)

lm_98105_inf <- lm(AdjSalePrice ~ SqFtTotLiving + SqFtLot + 
                     Bathrooms +  Bedrooms + BldgGrade,
                   subset=cooks_D<.08, data=house_98105)

# 아래부터 출력을 준비한다.
df <- data.frame(
  resid = residuals(lm_98105),
  pred = predict(lm_98105))

graph <- ggplot(df, aes(pred, abs(resid))) +
  geom_point() +
  geom_smooth(formula=y~x, method='loess') +
  scale_x_continuous(labels = function(x) format(x, scientific = FALSE)) +
  theme_bw()
filename <- "/tmp/sj223.jpg"
ggsave(file=filename)

# 차트 이름, 그리고 차트 자체(이미지 파일)을 df 에 추가 한다.

df$filename <- filename
lraw.lst <- vector("list", 1)
lraw.lst[[1L]] <- readBin(filename, "raw", file.info(filename)[1, "size"])
df$blob <- lraw.lst

df
```
