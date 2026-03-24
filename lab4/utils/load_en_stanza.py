import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import stanza

location = r"E:\Uni\Stanza"
stanza.download("en", model_dir=location)