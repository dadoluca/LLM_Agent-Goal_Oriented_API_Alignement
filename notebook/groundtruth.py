GENOME = {
    "name": "Genome Nexus",
    "link-readme": "https://github.com/WebFuzzing/EMB/tree/master/jdk_8_maven/cs/rest-gui/genome-nexus#readme",
    "swagger": "https://raw.githubusercontent.com/WebFuzzing/EMB/refs/heads/master/openapi-swagger/genome-nexus.json",
    "actors": [
        "Researchers", "Clinicians", "biologists", "Bioinformaticians", "Geneticists"
    ],
    "highLevelGoals":  ["Provide fast and automated annotation of genetic variants",
                "Enable high-throughput interpretation of genetic variants",
                "Integrate information from various existing resources",
                "Convert DNA changes to protein changes",
                "Predict functional effects of protein mutations",
                "Provide information about mutation frequencies",
                "Offer insights into gene function",
                "Detail variant effects",
                "Highlight clinical actionability of variants"],
    "lowLevelGoals": [
        # Provide a comprehensive one-stop resource for genetic variant annotation
        "Retrieve genetic variant data from multiple databases (e.g., dbSNP, ClinVar, COSMIC)",
        "Search and retrieve variant annotations from a user interface",
        "Annotate variants with clinical significance, mutation types, and related diseases",
        "Map genetic data to genome assemblies (e.g., GRCh38, hg19)",
        "Update variant information regularly from authoritative sources",
        
        # Enable fast and automated interpretation of cancer-related genetic variants
        "Analyze cancer-related mutations using automated tools",
        "Integrate gene expression data for cancer variant interpretation",
        "Identify cancer-related mutations linked to specific pathways",
        "Interpret large-scale cancer mutation datasets automatically",
        "Classify cancer mutations based on clinical relevance",
        
        # Support high-throughput analysis of genetic mutations
        "Process large genomic datasets in parallel",
        "Extract and transform mutation data from high-throughput sequencing formats (e.g., VCF, BAM)",
        "Perform mutation quality control and filtering",
        
        # Integrate data from multiple genomic databases
        "Fetch and harmonize data from various genomic databases",
        "Query integrated genomic databases for relevant mutation information",
        "Integrate multiple data sources with compatible formats for easy retrieval",
        
        # Convert DNA changes to corresponding protein changes
        "Map genetic mutations to corresponding protein-coding effects",
        "Convert mutations to amino acid changes for protein function analysis",
        "Predict the impact of mutations on protein structure using bioinformatics tools",
        
        # Predict the functional impact of protein mutations
        "Use prediction tools (e.g., PolyPhen, SIFT) to estimate mutation effects on protein function",
        "Build and apply machine learning models for functional impact prediction",
        "Rank mutations based on predicted severity of functional impact",
        
        # Provide information on mutation frequencies across datasets
        "Calculate mutation frequencies across various population groups",
        "Generate visual representations of mutation frequencies (e.g., histograms, pie charts)",
        "Provide mutation frequency data for specific diseases or conditions",
        
        # Offer insights into gene function and biological relevance
        "Retrieve gene function annotations from public databases like Gene Ontology (GO)",
        "Identify pathways and biological processes related to the mutated gene",
        "Link genetic variants to specific diseases or phenotypes based on annotations",
        
        # Detail the effects of genetic variants on protein function
        "Predict the effects of mutations on protein folding and stability",
        "Identify how mutations alter protein activity or structure",
        "Evaluate the impact of mutations on protein-protein interactions",
        
        # Highlight the clinical actionability of specific mutations
        "Link genetic mutations to clinical guidelines or treatment protocols",
        "Identify mutations with known clinical drug responses or therapeutic implications",
        "Provide actionable insights on mutations based on current clinical research"
    ]
}

GESTAO_HOSPITAL = {
    "name" : "Gestao Hospital",
    "link-readme": "https://github.com/ValchanOficial/GestaoHospital/blob/master/README.md",
    "swagger": "https://raw.githubusercontent.com/WebFuzzing/EMB/refs/heads/master/openapi-swagger/gestaohospital-rest.json",
    "actors": [
        "Hospital Manager",
        "Healthcare Staff",
        "Administrator",
        "Patients",
        "Hospital Logistics Staff",
    ],
    "highLevelGoals": [
        "Allow administrators and hospital managers to manage an hospital",
        "Allow hospital managers and healthcare staff to manage hospital beds and patients",
        "Allow healthcare staff to manage products and the blood bank",
        "Allow patients to look for hospitals",
    ],
    "lowLevelGoals" : [
        #"Allow administrators and hospital managers to manage an hospital",
        "Allow Registration of a New Hospital",
        "Allow Deletion of a Hospital",
        "Allow Modification of a Hospital",
        "Allow administrators to access statistics and manage indicators",
        "Enable hospital staff to manage appointment schedules",

        #"Allow patients to look for hospitals",
        "Recommend Nearest Hospital",
        "Return Information on a Hospital",

        #"Allow healthcare staff to manage products and the blood bank",
        "View Products and Quantities",
        "Allow logistic staff to Register Products",
        "Delete Products",
        "Allow logistic staff to change product quantities",
        "View Info on a Single Product",
        "Request a Product",
        "Allow searching for blood samples",

        #"Allow hospital managers and healthcare staff to manage hospital beds and patients",
        "Enable healthcare staff to view patient info and their medical history",
        "Register a Patient at a Hospital, entering personal information and contact info",
        "Allow patients to confirm their arrival at the ospital online or in presence"
        "Show estimated check in times for patient arriving at the hospital",
        "Allow healthcare staff to save notes regarding patients and their treatment in the system",
        "Change Patient Info and medical history",
    ]
}
