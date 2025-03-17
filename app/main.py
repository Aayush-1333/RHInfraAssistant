import gradio as gr
from telco_cloud_assist_crew.crew import TelcoCloudAssistCrew
from crewai.crew import CrewOutput
import warnings


## Gradio settings
HOST = 'localhost'
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def write_doc_file(*args) -> str:
    """
    Writes a doc file based on Crew's response
    """

    master_config, worker_config = args[0:4], args[4:]
    prompt_template = (
        "Create an RHOCP deployment low-level solution design based on the setup: "
        "\n**Master Nodes Conifguration**"
        f"\nNodes: {master_config[0]}"
        f"\nvCPUs per node: {master_config[1]}"
        f"\nRAM per node: {master_config[2]} GB"
        f"\nStorage size per node: {master_config[3]} GB"
        "\n\n**Worker Nodes Configuration**"
        f"\nNodes: {worker_config[0]}"
        f"\nvCPUs per node: {worker_config[1]}"
        f"\nRAM per node: {worker_config[2]} GB"
        f"\nStorage size per node: {worker_config[3]} GB"
        "\n\nTry to design this carefully."
    )
    # print(prompt_template)
    try:
        crew_response: CrewOutput = TelcoCloudAssistCrew().crew().kickoff(inputs={'requirements': prompt_template})
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
    with open("report.doc", "r") as f:
        f.read()
    print("[TOKEN USAGE]:", crew_response.token_usage)
    return f.name


## ==== UI Layout ====
with gr.Blocks(theme="default") as demo:
    ## App title
    gr.Markdown("# 🤖 Telco Cloud Accelerator")
    
    ## ============ Form layout ============
    ## Master Nodes
    with gr.Tab(label="Server Nodes Configuration"):
        with gr.Row():
            with gr.Column(variant="panel"):
                gr.Markdown("### Master Nodes Configuration")
                with gr.Row(variant="panel", elem_id="master"):
                    master_nodes = gr.Number(
                        label="Nodes", key="mast-nodes", 
                        value=3, minimum=3, maximum=15, step=2, interactive=True)
                    master_vcpu = gr.Number(
                        label="vCPUs per node", key="mast-vcpu", 
                        value=48, minimum=48, maximum=256, step=48, interactive=True)
                    master_ram = gr.Number(
                        label="RAM per node (in GBs)", key="mast-ram", 
                        value=256, minimum=256, maximum=1024, step=128, interactive=True)
                    master_stg = gr.Number(
                        label="Storage per node (in GBs)", key="mast-stg", 
                        value=512, minimum=256, maximum=2048, step=128, interactive=True)
                
                gr.Markdown("### Worker Nodes Configuration")
                with gr.Row(variant="panel", elem_id="worker"):
                    worker_nodes = gr.Number(
                        label="Nodes", key="worker-nodes", value=3, minimum=3, maximum=15, step=2, interactive=True)
                    worker_vcpu = gr.Number(
                        label="vCPUs per node", key="worker-vcpu", value=48, minimum=48, maximum=256, step=48, interactive=True)
                    worker_ram = gr.Number(
                        label="RAM per node (in GBs)", key="worker-ram", value=256, minimum=256, maximum=1024, step=128, interactive=True)
                    worker_stg = gr.Number(
                        label="Storage per node (in GBs)", key="worker-stg", value=512, minimum=256, maximum=2048, step=128, interactive=True)
            
                submit_btn = gr.Button("Submit")

            with gr.Column(variant="panel"):
                file_output = gr.File(label="Solution Document")

        submit_btn.click(fn=write_doc_file, inputs=[
            master_nodes, master_vcpu, master_ram, master_stg,
            worker_nodes, worker_vcpu, worker_ram, worker_stg
        ], outputs=file_output)


## ==== Driver Code ====
if __name__ == "__main__":
    demo.launch(share=False, pwa=True, width="60%")
