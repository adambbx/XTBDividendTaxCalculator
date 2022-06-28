## Podatek od zagranicznych dywidend XTB

Proste narzędzie do obliczania podatku (w PLN) od wypłaconych dywidend z zagranicznych aktywów (ETF-ów, akcji).

### Instalacja

Najpierw instalujemy zależności.

```bash
pip install -r requirements.txt
```

### Użycie

Skrypt uruchamiamy z wiersza poleceń.

Jako parametr `--csv_file` podajemy ścieżkę do pliku CSV z operacjami gotówkowymi z XTB. Plik csv powinnen mieć
następujące nagłówki `ID;Type;Time;Symbol;Comment;Amount`.

Jako parametr `--withholding_tax_file` podajemy ścieżkę do pliku w formacie JSON ze stawkami podatku u źródła dla
poszczególnych aktywów. Jeżeli można odliczyć podatek u źródła, należy umieścić symbol aktywa wraz
z wartością pobranego podatku (np. 0.15) w tym pliku. Na przykład, dostaliśmy dywidendę z akcji Tesli
notowanych na amerykańskiej giełdzie. 

```json
{
  "TSLA.US": 0.15
}
```

Przykładowe komenda.

```bash
python main.py --csv_file=transactions.csv --withholding_tax_file=withholding_taxes.json
```
