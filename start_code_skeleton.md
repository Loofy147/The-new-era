// 1. services/api-gateway/src/index.js
const express = require('express');
const bodyParser = require('body-parser');
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const app = express();
app.use(bodyParser.json());

// Load gRPC definitions
const packageDef = protoLoader.loadSync(
  __dirname + '/../../shared/proto/infer.proto',
  { keepCase: true }
);
const grpcPkg = grpc.loadPackageDefinition(packageDef).inference;
const grpcClient = new grpcPkg.Inference(
  'model-runner:50051', grpc.credentials.createInsecure()
);

// REST endpoint
app.post('/infer', async (req, res) => {
  const { model, input } = req.body;
  grpcClient.infer({ model, input }, (err, response) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(response);
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`API Gateway listening on ${PORT}`));


// 2. services/model-runner/src/infer.js
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const packageDef = protoLoader.loadSync(
  __dirname + '/../../shared/proto/infer.proto'
);
const grpcPkg = grpc.loadPackageDefinition(packageDef).inference;

function infer(call, callback) {
  const { model, input } = call.request;
  // TODO: load model and run inference
  const output = `Inference result for model ${model}`;
  callback(null, { output });
}

function main() {
  const server = new grpc.Server();
  server.addService(grpcPkg.Inference.service, { infer });
  server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
    server.start();
    console.log('ModelRunner gRPC server running on port 50051');
  });
}

main();


// 3. services/billing-engine/src/consumer.js
const { Kafka } = require('kafkajs');
const kafka = new Kafka({ clientId: 'billing-engine', brokers: ['broker:9092'] });
const consumer = kafka.consumer({ groupId: 'billing-group' });

async function run() {
  await consumer.connect();
  await consumer.subscribe({ topic: 'inference.events', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ message }) => {
      const event = JSON.parse(message.value.toString());
      // TODO: calculate billing
      console.log('Billing event:', event);
    },
  });
}

run().catch(console.error);


// 4. cli/src/index.js
#!/usr/bin/env node
const { program } = require('commander');

program
  .name('aimos')
  .description('AI-Model Marketplace CLI')
  .version('0.1.0');

program.command('list')
  .description('List available models')
  .action(() => {
    console.log('model1, model2, model3');
  });

program.command('run')
  .description('Run inference')
  .requiredOption('-m, --model <model>', 'Model name')
  .requiredOption('-i, --input <input>', 'Input data')
  .action((opts) => {
    console.log(`Running ${opts.model} on input: ${opts.input}`);
  });

program.parse(process.argv);


// 5. dashboard/src/App.jsx
import React, { useEffect, useState } from 'react';
import ModelList from './components/ModelList';

export default function App() {
  const [models, setModels] = useState([]);

  useEffect(() => {
    fetch('/api/models')
      .then(res => res.json())
      .then(setModels);
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">AI Model Marketplace</h1>
      <ModelList models={models} />
    </div>
  );
}


// 6. docker-compose.yml
version: '3.8'
services:
  api-gateway:
    build: ./services/api-gateway
    ports:
      - '3000:3000'
    depends_on:
      - model-runner

  model-runner:
    build: ./services/model-runner
    ports:
      - '50051:50051'

  billing-engine:
    build: ./services/billing-engine
    depends_on:
      - kafka

  kafka:
    image: bitnami/kafka:latest
    environment:
      - KAFKA_BROKER_ID=1
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
  zookeeper:
    image: bitnami/zookeeper:latest

  dashboard:
    build: ./dashboard
    ports:
      - '3001:3000'

  cli:
    build: ./cli
    entrypoint: ["node", "/usr/src/app/src/index.js"]

