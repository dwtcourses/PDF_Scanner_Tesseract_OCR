const SET_PDFS = 'SET_PDFS';

function pdfsReducer(state, action) {
    switch (action.type) {
        case SET_PDFS:
            state = action.payload;
            return state;
        default:
            return state
    }
}

export { pdfsReducer, SET_PDFS };