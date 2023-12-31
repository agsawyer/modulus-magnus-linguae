import lmql

def query(lmql_code):
    output = lmql.run_sync(lmql_code, output_writer=lmql.stream("RESPONSE"))
    return output

lmql_code = "argmax 'ANSWER KEY:[blue, green, red, yellow] Q: What color is the sky? A: [ANSWER]' from 'openai/davinci' where ANSWER in ['blue', 'green', 'red', 'yellow']"

query(lmql_code)

print(query(lmql_code))

# output[0].variables['ANSWER'].strip()

