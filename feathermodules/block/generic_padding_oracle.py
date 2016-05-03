import cryptanalib as ca
import feathermodules

padding_menu = """What kind of padding is being used?
1) PKCS#5/PKCS#7
2) ANSI X.923
3) ISO/IEC 7816-4:2005

Please enter a number: """

po_attack_script_skeleton = """# Generated by FeatherDuster
import cryptanalib as ca
import sys

if len(sys.argv) != 2:
   print '[*] Padding oracle attack script'
   print '[*] Usage: %%s <hex-encoded ciphertext or new plaintext>' %% sys.argv[0]

def padding_oracle(ciphertext):
   # TODO: Write a function to interact with the padding oracle
   # Pseudocode:
   # Send ciphertext to the padding oracle
   # If the padding oracle says the padding is good:
      return True
   # Otherwise, if the oracle says the padding is bad:
      return False

# To decrypt the first command line argument:
print "The decrypted version of your input is: " + ca.padding_oracle_decrypt(padding_oracle=padding_oracle, ciphertext=sys.argv[1].decode('hex'), block_size=%r, padding_type=%r, iv=%r, verbose=True, hollywood=%r)

# To encrypt the first command line argument:
# print "Your new ciphertext is: " + ca.cbcr(sys.argv[1].decode('hex'), oracle=padding_oracle, is_padding_oracle=True, block_size=%r, verbose=True)
"""

def generate_generic_padding_oracle_attack_script(ciphertexts):
   arguments = get_arguments(ciphertexts)
   while True:
      filename = raw_input('Please enter a file name for the padding oracle script: ')
      try:
         print '[+] Attempting to write script...'
         fh = open(filename, 'w')
         fh.write(po_attack_script_skeleton % (arguments['blocksize'],arguments['padding_type'],arguments['iv'],arguments['hollywood'],arguments['blocksize']))
         fh.close()
         break
      except:
         print '[*] Couldn\'t write to the file with the name provided. Please try again.'
         continue
   print '[+] Done! Your script is available at %s' % filename

def get_arguments(ciphertexts):
   arguments = {}
   arguments['ciphertexts'] = ciphertexts
   analysis_results = ca.analyze_ciphertext(ciphertexts)
   blocksize = analysis_results['blocksize']
   while True:
      print '[+] Block size detected as %d' % blocksize
      blocksize_answer = raw_input('Is this correct (yes)? ')
      if blocksize_answer.lower() in ['', 'yes', 'y']:
         arguments['blocksize'] = blocksize
         break
      else:
         blocksize_answer = raw_input('Please enter the correct blocksize: ')
         try:
            arguments['blocksize'] = int(blocksize_answer)
            break
         except:
            print '[*] Answer could not be interpreted as a number. Defaulting to detected block size.'
            arguments['blocksize'] = blocksize
            continue
   
   # If we actually supported anything but pkcs7, here we would do:
   # arguments['padding_type'] = raw_input(padding_menu)
   # But we don't, so we:
   arguments['padding_type'] = 'pkcs7'
   
   while True:
      iv_answer = raw_input('Do you want to specify an IV (no)? ')
      if iv_answer.lower() not in ['','n','no']:
         iv_hex = raw_input('What is the IV (hex encoded)?')
         try:
            iv_raw = iv_hex.decode('hex')
            if len(iv_raw) != arguments['blocksize']:
               arguments['iv'] = iv_raw
               break
            else:
               print '[*] Your IV does not match the blocksize of %d.' % arguments['blocksize']
               continue
         except:
            arguments['iv'] = None
            print '[*] You entered something that wasn\'t proper hex and wasn\'t \'no\'.'
            continue
      else:
         print '[+] Defaulting to all-null IV. If the IV is not a null block, expect the first block of output to be garbled.'
         arguments['iv'] = None
         break
   
   while True:
      prefix_answer = raw_input('Do you need to use a prefix (no)? ')
      if prefix_answer.lower() not in ['','n','no']:
         prefix = raw_input('Please enter the prefix you want to use, hex encoded: ')
         try:
            arguments['prefix'] = prefix.decode('hex')
            break
         except:
            print '[*] Couldn\'t decode your entry. Is it properly hex encoded?'
            continue
      else:
         arguments['prefix'] = ''
         break
   
   hollywood_answer = raw_input('Do you want hacker movie style output at a minor cost to performance (no I am lame)? ')
   arguments['hollywood'] = (hollywood_answer.lower() not in ['','n','no','no i am lame'])
 
   return arguments


feathermodules.module_list['padding_oracle'] = {
   'attack_function':generate_generic_padding_oracle_attack_script,
   'type':'block',
   'keywords':['block'],
   'description':'Generate a generic padding oracle attack script.'
}
