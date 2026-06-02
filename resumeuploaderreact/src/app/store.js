import { configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import { candidateApi } from '../services/candidateApi'

export const store = configureStore({
  reducer: {
    [candidateApi.reducerPath]: candidateApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(candidateApi.middleware),
})

setupListeners(store.dispatch)