/**
 * RTK Query API definition for candidate operations.
 *
 * Defines the ``candidateApi`` slice with a ``saveProfile`` mutation
 * that sends a POST request to the ``resume/`` endpoint for creating
 * new candidate profiles.
 */
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const candidateApi = createApi({
  reducerPath: 'candidateApi',
  baseQuery: fetchBaseQuery({ baseUrl: '127.0.0.1:8000/api/' }),
  endpoints: (builder) => ({
    saveProfile: builder.mutation({
      query: (candidate) =>{
        return {
            url: 'resume/',
            method:'POST',
            body:candidate
        }
      } ,
    }),
  }),
})


// export const { useSaveProfileQuery } = candidateApi
export const { useSaveProfileMutation } = candidateApi