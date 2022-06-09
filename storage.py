from docarray import DocumentArray

lipstick_db = DocumentArray(storage='annlite', config={
    'data_path': './data',
    'n_dim': 18 + 16 + 16,
})
