import mlflow
import dagshub
import sys

def download_model(path):
    dagshub.init(repo_owner='joycesafg', repo_name='DataMaster_Case', mlflow=True)
    mlflow.set_tracking_uri(uri="https://dagshub.com/joycesafg/DataMaster_Case.mlflow")

    try:
        mlflow.artifacts.download_artifacts(run_id="629006b8e630475f98b6c1a5f0dc7143", dst_path=path)
    except Exception as e:
        print(f"Error: {e}")

    return path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        download_model(path)
    else:
        print("No path parameter provided")