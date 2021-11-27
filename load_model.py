

# load model for Google Drive
model.model = load_model("model/key_classifier.h5")

# import unseen data to check if model works
pred_df = pd.read_csv(TEST_DATA_LINK)
pred_df.head()

pred_dataset = pred_df.values

# divide data into features X
# X_new = new_dataset[:,3:].astype(float)

pred_row=pred_df.iloc[:,3:]
# print("check name")
# print(pred_df.iloc[0:7,0:1])

# convert to
pred_row = pred_row.values.tolist()
pred_row = scaler.transform(pred_row)
pred_arr = np.asarray(pred_row, dtype=np.float32)
pred_arr = np.reshape(pred_arr, (pred_row.shape[0], TIMESTEPS, pred_arr.shape[1]))

# get prediction and its label
pred = model.predict(pred_arr)
pred = to_categorical(pred)
pred = encoder.inverse_transform(pred)

pred = np.squeeze(pred)

pred_proba = model.predict_proba(pred_arr)
acc = np.max(pred_proba, axis=1)

print(pred)
print(acc)