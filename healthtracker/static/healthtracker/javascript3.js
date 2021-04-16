document.addEventListener('DOMContentLoaded', () => {

})

function post()
{
    fetch(`/patientsdataapi`, {
        method: 'POST',
        body: JSON.stringify({
            fname: "testingapi",
            lname: "testingapi",
            rnumber: 100,
            gender: "male",
            state: "Punjab",
            streetaddress: "Thapar University, Patiala"
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result.message)
        })
}

function post2()
{
    fetch(`/patientsstatusapi/REG20201`, {
        method: 'POST',
        body: JSON.stringify({
            pulserate: 90,
            temperature: 98.7
        })
    })
        .then(response => response.json())
        .then(result => {
            console.log(result.message)
        })
}

function displaydata(regnumber)
{
    let table = document.querySelector('#data-table');
    let header = table.insertRow(0);
    let cell4 = header.insertCell(0);
    let cell1 = header.insertCell(1);
    let cell2  = header.insertCell(2);
    let cell3  = header.insertCell(3);
    cell1.innerHTML = "Pulse Rate (BPM)";
    cell2.innerHTML = "Temperature (F)";
    cell3.innerHTML = "Time";
    cell4.innerHTML = "#";
    cell1.scope = 'col';
    cell2.scope = 'col';
    cell3.scope = 'col';
    cell4.scope = 'col';
    fetch(`/patientsstatusapi/${regnumber}`)
        .then(response => response.json())
        .then(data => {
            let i = 0;
            let j = 1;
            let k = 0
            if(data.length < 10)
            {
                k = data.length
            }
            else
                k = 10
            for(i = 0; i < 10; i++)
            {
                let newrow = table.insertRow(j);
                let newcell4 = newrow.insertCell(0);
                let newcell1 = newrow.insertCell(1);
                let newcell2 = newrow.insertCell(2);
                let newcell3 = newrow.insertCell(3);

                newcell1.innerHTML = `${data[i].pulserate}`;
                newcell2.innerHTML = `${data[i].temperature}`;
                newcell3.innerHTML = `${data[i].time}`;
                newcell4.innerHTML = `${j}`;
                newcell4.scope = 'row';
                j++;
            }
        });
}