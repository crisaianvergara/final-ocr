import Head from "next/head";
import { useState } from "react";
import { Table, Button, Form, Upload, message } from "antd";
import { InboxOutlined } from "@ant-design/icons";

const { Dragger } = Upload;

export const getStaticProps = async () => {
    const res = await fetch("http://127.0.0.1:8000/scans/api/");
    const data = await res.json();

    return {
        props: { receipts: data },
    };
};

const ScanReceipt = ({ receipts: initialReceipts }) => {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [receipts, setReceipts] = useState(initialReceipts);

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("image", file);
        setUploading(true);
        try {
            const response = await fetch("http://127.0.0.1:8000/scans/api/", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            console.log(data);
            setReceipts([data, ...receipts]);
            setFile(null);
            message.success("Receipt scanned successfully.");
        } catch (error) {
            console.error(error);
            message.error("Error during upload.");
        }
        setUploading(false);
    };

    const columns = [
        {
            title: "Date",
            dataIndex: "date",
            key: "date",
        },
        {
            title: "Vendor",
            dataIndex: "vendor",
            key: "vendor",
        },
        {
            title: "Amount",
            dataIndex: "amount",
            key: "amount",
        },
        {
            title: "Tax",
            dataIndex: "tax",
            key: "tax",
        },
        {
            title: "Currency",
            dataIndex: "currency",
            key: "currency",
        },
        {
            title: "Description",
            dataIndex: "description",
            key: "description",
        },
    ];

    return (
        <>
            <Head>
                <title>Zia Apps | Scan Receipt</title>
                <meta name="keywords" content="zia apps" />
            </Head>
            <div>
                <h1>Scan Receipt</h1>
                <Form>
                    <Form.Item>
                        <Dragger
                            beforeUpload={(file) => {
                                setFile(file);
                                return false;
                            }}
                        >
                            <p className="ant-upload-drag-icon">
                                <InboxOutlined />
                            </p>
                            <p className="ant-upload-text">
                                Click or drag file to this area to upload
                            </p>
                            <p className="ant-upload-hint">Support for a single upload.</p>
                        </Dragger>
                    </Form.Item>
                    <Form.Item>
                        <Button
                            type="primary"
                            htmlType="submit"
                            onClick={handleUpload}
                            disabled={!file || uploading}
                        >
                            Scan Receipt
                        </Button>
                    </Form.Item>
                </Form>
                <Table dataSource={receipts} columns={columns} rowKey="id" />
            </div>
        </>
    );
};

export default ScanReceipt;
