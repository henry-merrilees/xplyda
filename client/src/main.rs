use embedding::embedding_service_client::EmbeddingServiceClient;
use embedding::EmbeddingRequest;

use anyhow::Result;

pub mod embedding {
    tonic::include_proto!("embedding");
}

#[allow(unreachable_code)]
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let delay_duration = std::time::Duration::from_secs(2);
    let mut client = loop {
        let connection = EmbeddingServiceClient::connect("http://embedding_service:50052").await;
        match connection {
            Ok(inner) => break inner,
            Err(e) => {
                println!("Error: {:?}", e);
                println!("Retrying in {:?}...", delay_duration);
                tokio::time::sleep(delay_duration).await;
                continue;
            }
        };
    }
    .max_decoding_message_size(usize::MAX)
    .max_encoding_message_size(usize::MAX);

    let sentiment = [
        "This is a sentence about positive things.",
        "This is a sentence about negative things.",
    ]
    .map(String::from)
    .to_vec();

    let test = [
        "I hate puppies.",
        "I am happy with the world around me.",
        "Have you seen that new movie? I think it sucks.",
        "I don't really have a favorite food. I like all food.",
    ]
    .map(String::from)
    .to_vec();

    let sentiment_request = tonic::Request::new(EmbeddingRequest { texts: sentiment });
    let sentiment_response = client.generate_embeddings(sentiment_request).await?;
    let sentiment_embeddings: Vec<Vec<f32>> = sentiment_response
        .into_inner()
        .embeddings
        .into_iter()
        .map(|e| e.values)
        .collect();

    let test_request = tonic::Request::new(EmbeddingRequest {
        texts: test.clone(),
    });
    let test_response = client.generate_embeddings(test_request).await?;
    let test_embeddings: Vec<Vec<f32>> = test_response
        .into_inner()
        .embeddings
        .into_iter()
        .map(|e| e.values)
        .collect();

    for (message, embedding) in test.iter().zip(test_embeddings.iter()) {
        let positive_score = dot(embedding, &sentiment_embeddings[0]);
        let negative_score = dot(embedding, &sentiment_embeddings[1]);
        let score = (positive_score - negative_score) / (positive_score + negative_score);
        println!("Message: {} -- sentiment: {}", message, score);
    }
    Ok(())
}

fn dot(v1: &[f32], v2: &[f32]) -> f32 {
    v1.iter().zip(v2.iter()).map(|(a, b)| a * b).sum()
}
