const URL = "https://fibar.elixir.ut.ee/"

export default {

    baseURL: URL,

    async upload(formData, callback) 
        {
        fetch(`${URL}api/upload`, {
            method: 'POST',
            body: formData
        }).then((response) => {
             return response.json();
        }).then((json) => {
            callback(json);
        }).catch((error) => {
            console.error(error);
        });
        },

    async analyze(params, callback = () => {
    }) {
        fetch(`${URL}api/analyze`, {
            method: 'POST',
            //timeout: 360000,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(params)
        }).then((response) => {
            return response.json();
        }).then((json) => {
            callback(json);
        }).catch(function (err) {
            console.log('Fetch problem: ' + err.message);
        });
    },

    async results_update(params, callback = () => {
    }) {
        fetch(`${URL}api/results_update`, {
            method: 'POST',
            //timeout: 360000,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(params)
        }).then((response) => {
            return response.json();
        }).then((json) => {
            callback(json);
        }).catch(function (err) {
            console.log('Fetch problem: ' + err.message);
        });
    },

};
