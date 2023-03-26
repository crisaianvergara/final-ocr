import Head from "next/head";
import { Table, Button, Form, Upload } from 'antd'
import { InboxOutlined } from '@ant-design/icons';

const { Dragger } = Upload;

export const getStaticProps = async () => {
  const res = await fetch('http://127.0.0.1:8000/scans/api/');
  const data = await res.json();

  return {
    props: { receipts: data }
  }
}

const ScanReceipt = ({receipts}) => {
    const columns = [
        {
            title: 'Date',
            dataIndex: 'date',
            key: 'date'
        },
        {
            title: 'Vendor',
            dataIndex: 'vendor',
            key: 'vendor'
        },
        {
            title: 'Amount',
            dataIndex: 'amount',
            key: 'amount'
        },
        {
            title: 'Tax',
            dataIndex: 'tax',
            key: 'tax'
        },
        {
            title: 'Currency',
            dataIndex: 'currency',
            key: 'currency'
        },
        {
            title: 'Description',
            dataIndex: 'description',
            key: 'description'
        }
    ]
    
    return ( 
        <>
            <Head>
                <title>Zia Apps | Scan Receipt</title>
                <meta name='keywords' content='zia apps'/>
            </Head>  
            <div>
                <h1>Scan Receipt</h1>
                <Form>
                    <Form.Item>
                        <Dragger>
                            <p className="ant-upload-drag-icon">
                                <InboxOutlined />
                            </p>
                            <p className="ant-upload-text">Click or drag file to this area to upload</p>
                            <p className="ant-upload-hint">Support for a single upload.</p>
                        </Dragger>
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">
                            Scan Receipt
                        </Button>
                    </Form.Item>
                </Form>
                <Table dataSource={receipts} columns={columns} rowKey="id" />
            </div>
        </>
     );
}
 
export default ScanReceipt;
