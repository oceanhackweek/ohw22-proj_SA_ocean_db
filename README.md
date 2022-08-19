# &#127754; Public Ocean Database for South Atlantic

# OHW22_SA_ocean_db
---
## &#128221; One line description
Bridge ocean data gaps across the Brazilian coast and make it easily available to the public.

### 👥 Collaborators

Danilo Augusto Silva - [nilodna](https://github.com/nilodna)

Denise Fukai - [denisefukai](https://github.com/denisefukai)

Douglas M. Nehme - [douglasnehme](https://github.com/douglasnehme)

Filipe Fernandes - [ocefpaf](https://github.com/ocefpaf)

Luiza Paschoal Stein - [LuizaPS](https://github.com/LuizaPS)

Marcela Strane - [marcela-strane](https://github.com/marcela-strane)

Paula Marangoni - [paulamarangoni](https://github.com/paulamarangoni)

Tobias Ramalho dos Santos Ferreira - [soutobias](https://github.com/soutobias)

---
### &#128129; Background
The South Atlantic is one of the least observed oceans globally. It has several socio-economic impacts for bordering countries, from less accurate daily metocean weather forecasts to problems in seasonal forecasting of food crops, for example. The growth of worldwide ocean observing programs based on autonomus equipment such as [profilers](https://argo.ucsd.edu/) and [drifters](https://www.aoml.noaa.gov/global-drifter-program/) has greatly increased *in situ* observations in the role ocean basin. But for a comprehensive understanding of the South Atlantic other long-term and multi-parameter data from the entire water column are essential. For Brazilian waters, public data from weather buoys, CTDs, ADCPs and others  are still rare and those that exist are tightly dispersed across diferent institutions. This, in practice, means that these data do not exist for the community and do not bring any relevant gain to society.

### &#127919; Goals
Gather disperse oceaneanographic data for the South Atlantic and make it easily available for the public.

### &#127942; Relevance
- Fulfillment:
  - #6 [United Nations Ocean Decade Goal](https://www.oceandecade.org/vision-mission/)
    - An accessible ocean with open and equitable access to data, information and technology and innovation

- Contribute to:
  - #13, #14, and #15 [United Nations Sustainable Development Goals](https://sdgs.un.org/goals#goals)
    - [#13](https://sdgs.un.org/goals/goal13): Take urgent action to combat climate change and its impacts
    - [#14](https://sdgs.un.org/goals/goal14): Conserve and sustainably use the oceans, seas and marine resources for sustainable development
    - [#15](https://sdgs.un.org/goals/goal15): Protect, restore and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, and halt and reverse land degradation and halt biodiversity loss

### &#128290; Datasets
- [Brazilian National Buoy Program - PNBOIA](https://www.marinha.mil.br/chm/dados-do-goos-brasil/pnboia)
  - The main Brazilian buoy program that is manage by the Brazilian Navy with suport of a multi-institutional national board. PNBOIA is one of the Brazilian efforts for [The Global Ocean Observing System - GOOS](https://www.goosocean.org/) and the [Regional Alliance in Oceanography for the Upper Southwest and Tropical Atlantic - OCEATLAN](http://www.oceatlan.org/).

### &#128256; Workflow

- Gather weather buoy data;

- Apply QC measures to the data;

- Host the QC data into a SQL database;

- Connect the SQL database to a API;

- Make the API public.

### &#128679; Future Developments

- Map public ocean data for South Atlantic Ocean that is not delivered in a easy and/or programmatic way.
  - Already planned datasets:
    - [Prediction and Research Moored Array in the Tropical Atlantic - PIRATA](https://www.pmel.noaa.gov/gtmba/pmel-theme/atlantic-ocean-pirata)
    - [Monitoring System of the Brazilian Coast - SiMCosta](https://simcosta.furg.br/home)

[comment]: <> (### &#128218; References)
