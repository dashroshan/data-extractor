import { useState, useEffect } from "react";
import axios from "axios";

export default function App() {
    const [file, setFile] = useState(null);
    const [data, setData] = useState(null);
    const [csvData, setCsvData] = useState(null);
    const [loading, setLoading] = useState(true);

    const fileUploadHandler = (e) => {
        if (e.target.files) setFile(e.target.files[0]);
    }

    useEffect(() => {
        async function doTask() {
            try {
                if (!file) return;
                let formData = new FormData();
                formData.append("file", file);
                const { data: data } = await axios.post('/api/uploadForm', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                if (data.status !== "succeeded") return;
                data.obj.paragraphs.shift();
                data.obj.keyValuePairs.shift();
                setData(data.obj);
                setCsvData(data.csv);
                setLoading(false);
            } catch (error) {
                console.log(error)
            }
        }
        doTask();
    }, [file])

    function downloadCSV(data) {
        var dataStr = "data:text/csv;charset=utf-8," + data;
        console.log(dataStr);
        var downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "export.csv");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    }

    const resetPage = () => {
        setData(null);
        setCsvData(null);
        setLoading(true);
        setFile(null);
    }

    return (
        <div class="bg-base-200 min-h-screen px-2">
            <div class="hero py-16">
                <div class="hero-content text-center">
                    <div class="max-w-md">
                        <h1 class="text-5xl font-bold">Data Extractor</h1>
                        <p class="py-6">Upload your form in PDF, PNG, or JPG format to extract the key-value pairs, tables, and paragraphs into CSV file.</p>
                        {!file ? <input type="file" onChange={fileUploadHandler} accept=".jpg,.jpeg,.png,.pdf" class="file-input file-input-bordered file-input-primary w-full max-w-xs" />
                            : (loading ? <div class="bg-primary loading loading-infinity loading-lg block mx-auto scale-[3] my-10"></div> : <button class="btn btn-primary" onClick={resetPage}>
                                <svg xmlns="http://www.w3.org/2000/svg" height="1.4em" viewBox="0 0 512 512"><path fill="#fff" d="M105.1 202.6c7.7-21.8 20.2-42.3 37.8-59.8c62.5-62.5 163.8-62.5 226.3 0L386.3 160H336c-17.7 0-32 14.3-32 32s14.3 32 32 32H463.5c0 0 0 0 0 0h.4c17.7 0 32-14.3 32-32V64c0-17.7-14.3-32-32-32s-32 14.3-32 32v51.2L414.4 97.6c-87.5-87.5-229.3-87.5-316.8 0C73.2 122 55.6 150.7 44.8 181.4c-5.9 16.7 2.9 34.9 19.5 40.8s34.9-2.9 40.8-19.5zM39 289.3c-5 1.5-9.8 4.2-13.7 8.2c-4 4-6.7 8.8-8.1 14c-.3 1.2-.6 2.5-.8 3.8c-.3 1.7-.4 3.4-.4 5.1V448c0 17.7 14.3 32 32 32s32-14.3 32-32V396.9l17.6 17.5 0 0c87.5 87.4 229.3 87.4 316.7 0c24.4-24.4 42.1-53.1 52.9-83.7c5.9-16.7-2.9-34.9-19.5-40.8s-34.9 2.9-40.8 19.5c-7.7 21.8-20.2 42.3-37.8 59.8c-62.5 62.5-163.8 62.5-226.3 0l-.1-.1L125.6 352H176c17.7 0 32-14.3 32-32s-14.3-32-32-32H48.4c-1.6 0-3.2 .1-4.8 .3s-3.1 .5-4.6 1z" /></svg>
                                RESET
                            </button>)}
                    </div>
                </div>
            </div>

            {data ?
                <div class="card max-w-5xl mx-auto bg-white drop-shadow-md p-6">
                    <h1 class="text-3xl font-bold text-center">Key-value pairs</h1>
                    <div class="divider"></div>

                    <div class="overflow-x-auto">
                        <table class="table">
                            <tbody>
                                <tr>
                                    <th>Key</th>
                                    <th>Value</th>
                                </tr>
                                {data.keyValuePairs.map(kv => <tr>
                                    <td>{kv[0]}</td>
                                    <td>{kv[1]}</td>
                                </tr>)}
                            </tbody>
                        </table>
                    </div>
                </div> : null}

            {data ?
                <div class="card max-w-5xl mx-auto bg-white drop-shadow-md p-6 mt-10">
                    <h1 class="text-3xl font-bold text-center">Tables</h1>
                    {data.tables.map((table, i) => <>
                        <div class="divider">{i + 1}</div>

                        <div class="overflow-x-auto">
                            <table class="table">
                                <tbody>
                                    {table[0].map((row, j) =>
                                        <tr>
                                            {row.map(item =>
                                                (table[1] >= j) ?
                                                    <th>{item}</th> :
                                                    <td>{item}</td>
                                            )}
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </>)}
                </div> : null}


            {data ?
                <div class="card max-w-5xl mx-auto bg-white drop-shadow-md p-6 mt-10">
                    <h1 class="text-3xl font-bold text-center">Paragraphs</h1>
                    <div class="divider"></div>

                    <div class="overflow-x-auto">
                        <table class="table">
                            <tbody>
                                {data.paragraphs.map(p => <tr><td>{p[0]}</td></tr>)}
                            </tbody>
                        </table>
                    </div>
                </div>
                : null
            }

            {csvData ?
                <div class="text-center py-10">
                    <button class="btn btn-primary" onClick={() => downloadCSV(csvData)}>
                        <svg xmlns="http://www.w3.org/2000/svg" height="1.4em" viewBox="0 0 448 512"><path fill="#fff" d="M64 32C28.7 32 0 60.7 0 96V416c0 35.3 28.7 64 64 64H384c35.3 0 64-28.7 64-64V173.3c0-17-6.7-33.3-18.7-45.3L352 50.7C340 38.7 323.7 32 306.7 32H64zm0 96c0-17.7 14.3-32 32-32H288c17.7 0 32 14.3 32 32v64c0 17.7-14.3 32-32 32H96c-17.7 0-32-14.3-32-32V128zM224 288a64 64 0 1 1 0 128 64 64 0 1 1 0-128z" /></svg>
                        DOWNLOAD CSV
                    </button>
                </div> : null}
        </div>
    );
}
