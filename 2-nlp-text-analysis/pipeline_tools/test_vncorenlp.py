import py_vncorenlp

try:
    # Initialize the tokenizer
    # Assuming the models are downloaded in the current directory or 'VnCoreNLP'
    rdrsegmenter = py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir='d:/PROJECT/phantichdulieu/VnCoreNLP')
    
    unaccented_text = "Toi rat hai long voi dich vu cua nguoi ban va shipper lan nay."
    accented_text = "Tôi rất hài lòng với dịch vụ của người bán và shipper lần này."
    
    print("--- TEXT KHÔNG DẤU ---")
    print(rdrsegmenter.word_segment(unaccented_text))
    
    print("\n--- TEXT CÓ DẤU ---")
    print(rdrsegmenter.word_segment(accented_text))
    
except Exception as e:
    print(f"Error: {e}")
