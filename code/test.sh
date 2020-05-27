#!/usr/bin/env bash


# Test 1: Does it run to completion?
python best_science_ever.py split test_data.csv 2>/dev/null 1>/dev/null
if [ $? -eq 0 ]
then
  echo "Test passed!"
else
  echo "Test failed!"
fi

# Optionally, something like this: test $? -eq 0 || echo "something bad happened"
# https://stackoverflow.com/questions/26675681/how-to-check-the-exit-status-using-an-if-statement

# Test 2: in a perfect world, splitting with 10 rows (> our original DF),
# the input and output would be identical
diff test_data.csv test_data_0_processed.csv 2>/dev/null 1>/dev/null
if [ $? -eq 0 ]
then
  echo "Test passed!"
else
  echo "Test failed!"
fi
