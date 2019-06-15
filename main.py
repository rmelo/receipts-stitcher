import subprocess

subprocess.run(['stitcher Default target-receipt.jpeg ./data/receipts/01/low/*.jpeg'], shell=True)

print('Done!')
