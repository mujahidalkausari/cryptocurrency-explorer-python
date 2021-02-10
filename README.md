# cryptocurrency-explorer-python
The script take address and ticker as input, make repective API calls, create JSON ouput and save data to CSV report file.

Updates:
The following two apis added to the script and tested...there are two records for each against the listed Tickers in the Addresses input file.

ETC: https://blockscout.com/etc/mainnet/api-docs and EWT: https://explorer.energyweb.org/api-docs

AND

The following issues done...

1. Remove the need for subdirectories. I like to keep both input and output file in the main directory.
2. Date column must include time
3. Output file must be called Balance report.csv and follow the specification (order of columns: Ticker,Address,Balance,Date)
4. Please limit the balance output to only the main ticker, i.e. for NEO -&gt; NEO and ONT -&gt; ONT
5. Remove debug output (or make it configurable using an internal variable)
