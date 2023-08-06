# -*- coding: utf-8 -*-
#
# Copyright 2021 Compasso UOL
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Reader Class Implementation"""
from dora_parser.parser import Parser
from dora_parser.transpiler import Transpiler
from mo_parsing.exceptions import ParseException
from dora_parser.report import Report
from dora_parser import logger
from collections import Counter
import re
import os
from pathlib import Path

SUPPORTED_DIALECTS = ['impala-spark','impala-presto']

class Reader():
    def __init__(self, from_dialect:str, to_dialect:str, input_dir:str=None, output_dir:str = None, migration_report:bool = False):
        """Initialize the reader class
        :param from_dialect: From SQL dialect
        :param to_dialect: To SQL dialect
        :param input_dir: Input Directory
        :param output_dir: Output Directory
        :param migration_report: If true, creates the migration report
        """
        self.from_dialect = str(from_dialect).lower()
        self.to_dialect = str(to_dialect).lower()
        if self.from_dialect not in ['impala'] or self.to_dialect not in ['spark','presto']:
            raise ValueError(f"Only the following dialects are supported:{SUPPORTED_DIALECTS}")
        self.input_dir =  input_dir
        self.output_dir = self.input_dir if output_dir is None else output_dir
        self.migration_report = migration_report
        self.regex = {
                        "impala-presto": {
                                "not_allowed": {  "ALTER DATABASE" : r"^(ALTER(\s*)DATABASE)",
                                                  "ALTER TABLE ADD IF NOT EXISTS COLUMNS": r'^(ALTER(\s*)TABLE(.|\n)*?ADD(\s*)(IF(\s*)NOT(\s*)EXISTS)(\s*)COLUMNS)',
                                                  "ALTER TABLE ADD COLUMN":r"^(ALTER(\s*)TABLE(.|\n)*?ADD(\s*)(COLUMN ))",
                                                  "ALTER TABLE ADD COLUMNS WITH COMMENT OR KUDU_ATTRIBUTES":r"^(ALTER(\s*)TABLE(.|\n)*?ADD(.|\n)*?COLUMNS(.|\n)*?(COMMENT|NULL|COMPRESSION|DEFAULT|BLOCK_SIZE|ENCODING))",
                                                  "ALTER TABLE ADD PARTITION WITH CACHED":r"^(ALTER(\s*)TABLE(.|\n)*?ADD(.|\n)*?PARTITION(.|\n)*?(CACHED(\s*)IN ))",
                                                  "ALTER TABLE ALTER":r"^(ALTER(\s*)TABLE(.|\n)*?(ALTER ))",
                                                  "ALTER TABLE DROP":r"^(ALTER(\s*)TABLE(.|\n)*?DROP(\s*)(?!.*PARTITION))",
                                                  "ALTER TABLE DROP PARTITION":r"^(ALTER(\s*)TABLE(.|\n)*?DROP(.|\n)*?PARTITION(.|\n)*?(PURGE))",
                                                  "ALTER TABLE CHANGE":r"^(ALTER(\s*)TABLE(.|\n)*?CHANGE )",
                                                  "ALTER TABLE SET CACHED IN OR UNCACHED":r"^(ALTER(\s*)TABLE(.|\n)*?SET(\s*)(UNCACHED|CACHED(\s*)IN ))",
                                                  "ALTER TABLE SET FILEFORMAT":r'^(ALTER(\s*)TABLE(.|\n)*?SET(\s*)(FILEFORMAT))',
                                                  "ALTER TABLE SET SERDEPROPERTIES":r"^(ALTER(\s*)TABLE(.|\n)*?SET(\s*)(SERDEPROPERTIES))",
                                                  "ALTER TABLE SET ROW FORMAT":r"^(ALTER(\s*)TABLE(.|\n)*?SET(\s*)(ROW(\s*)FORMAT))",
                                                  "ALTER TABLE SET OWNER USER":r"^(ALTER(\s*)TABLE(.|\n)*?(SET(\s*)OWNER(\s*)USER ))",
                                                  "ALTER TABLE RANGE PARTITION":r"^(ALTER(\s*)TABLE(.|\n)*?(RANGE(\s*)PARTITION ))",
                                                  "ALTER TABLE RECOVER PARTITIONS":r"^(ALTER(\s*)TABLE(.|\n)*?(RECOVER(\s*)PARTITIONS))",
                                                  "ALTER TABLE REPLACE COLUMNS WITH COMMENT OR KUDU_ATTRIBUTES":r"^(ALTER(\s*)TABLE(.|\n)*?REPLACE(\s*)COLUMNS(.|\n)*?(COMMENT|NULL|COMPRESSION|DEFAULT|BLOCK_SIZE|ENCODING))",
                                                  "ALTER TABLE RENAME TO":r"^(ALTER(\s*)TABLE(.|\n)*?(RENAME(\s*)TO ))",
                                                  "ALTER TABLE WITH STATSKEY":r"^(ALTER(\s*)TABLE(.|\n)*?(numDVs|numNulls|avgSize|maxSize))",
                                                  "ALTER VIEW" : r"^(ALTER(\s*)VIEW)",
                                                  "COMPUTE STATS":r"^(COMPUTE(.|\n)*?STATS)",
                                                  "COMMENT (START WITH)":r"^(COMMENT)",
                                                  "CREATE FUNCTION":r"^(CREATE(.|\n)*?FUNCTION)",
                                                  "CREATE TABLE AS SELECT":r"^(CREATE(.|\n)*?TABLE(.|\n)*?(AS(\s*)SELECT))",
                                                  "CREATE TABLE EXCEPTIONS":r"^(CREATE(.|\n)*?TABLE(.|\n)*?(PRIMARY(\s*)KEY|FOREIGN(\s*)KEY|SORT(\s*)BY|CACHED(\s*)IN ))",
                                                  "CREATE TABLE LIKE":r"^(CREATE(.|\n)*?TABLE(.|\n)*?(LIKE))",
                                                  "CREATE TABLE KUDU EXCEPTIONS":r"^(CREATE(.|\n)*?TABLE(.|\n)*?(PRIMARY(\s*)KEY|NULL |ENCODING|COMPRESSION|DEFAULT|BLOCK_SIZE|PARTITION(\s*)BY ))",
                                                  "CREATE ROLE":r"^(CREATE(\s*)ROLE)",
                                                  "CREATE VIEW": r"^(CREATE(\s*)VIEW(.|\n)*?(IF(\s*)NOT(\s*)EXISTS|COMMENT|\((.+)\))(.|\n)*?AS(\s*)SELECT)",
                                                  "DELETE":r"^(DELETE)",
                                                  "DESCRIBE DATABASE":r"^(DESCRIBE(.|\n)*?DATABASE)",
                                                  "DROP FUNCTION":r"^(DROP(\s*)FUNCTION)",
                                                  "DROP ROLE":r"^(DROP(\s*)ROLE)",
                                                  "DROP STATS":r"^(DROP(.|\n)*?STATS)",
                                                  "DROP TABLE PURGE":r"^(DROP(\s*)TABLE(.|\n)*?PURGE)",
                                                  "GRANT":r"^(GRANT)",
                                                  "INSERT":r"^(INSERT(.|\n)*?(TABLE |OVERWRITE|PARTITION|VALUES))",
                                                  "INVALIDATE METADATA":r"^(INVALIDATE(\s*)METADATA)",
                                                  "OPTIMIZER HINTS":r"(BROADCAST|SHUFFLE|NOSHUFFLE|SCHEDULE_CACHE_LOCAL|SCHEDULE_DISK_LOCAL|SCHEDULE_REMOTE|CLUSTERED|NOCLUSTERED)",
                                                  "LOAD DATA":r"^(LOAD(\s*)DATA )",
                                                  "REFRESH":r"^(REFRESH)",
                                                  "REVOKE":r"^(REVOKE)",
                                                  "SET":r"^(SET)",
                                                  "SHOW EXCEPTIONS":r"^(SHOW(.|\n)*?(TABLES(.|\n)*?LIKE |FUNCTIONS|GRANT|ROLES|ROLE|FILES(\s*)IN|RANGE|COLUMN(\s*)STATS|TABLE(\s*)STATS))",
                                                  "SHUTDOWN":r"^(:SHUTDOWN)",
                                                  "TRUNCATE":r"^(TRUNCATE)",
                                                  "USE":r"^(USE)",
                                                  "UPDATE":r"^(UPDATE)",
                                                  "UPSERT":r"^(UPSERT)",
                                                  "VALUES (START WITH)":r"^(VALUES)",
                                                  "USE":r"^(USE)",
                                                  "WITH INSERT":r"^(WITH(.|\n)*?INSERT)"

                                                },
                                
                                "replace": {
                                                "CREATE EXTERNAL TABLE" : "CREATE TABLE",
                                                "REAL" : "FLOAT"
                                           }
                                  },
        
                        "impala-spark": {

                                "not_allowed": {  "ALTER DATABASE" : r"^(ALTER(\s*)DATABASE )",
                                                  "ALTER TABLE ADD IF NOT EXISTS COLUMNS": r'^(ALTER(\s*)TABLE(.|\n)*?ADD(\s*)(IF(\s*)NOT(\s*)EXISTS)(\s*)COLUMNS)',
                                                  "ALTER TABLE ADD COLUMN":r"^(ALTER(\s*)TABLE(.|\n)*?ADD(\s*)(COLUMN ))",
                                                  "ALTER TABLE ADD COLUMNS WITH COMMENT OR KUDU_ATTRIBUTES":r"^(ALTER(\s*)TABLE(.|\n)*?ADD(.|\n)*?COLUMNS(.|\n)*?(COMMENT|NULL|COMPRESSION|DEFAULT|BLOCK_SIZE|ENCODING))",
                                                  "ALTER TABLE CHANGE WITH COMMENT OR KUDU_ATTRIBUTES":r"^(ALTER(\s*)TABLE(.|\n)*?CHANGE(.|\n)*?(COMMENT|NULL|COMPRESSION|DEFAULT|BLOCK_SIZE|ENCODING))",
                                                  "ALTER TABLE ADD PARTITION WITH LOCATION OR CACHE":r"^(ALTER(\s*)TABLE(.|\n)*?ADD(.|\n)*?PARTITION(.|\n)*?(LOCATION|CACHED(\s*)IN ))",
                                                  "ALTER TABLE ALTER":r"^(ALTER(\s*)TABLE(.|\n)*?(ALTER ))",
                                                  "ALTER TABLE DROP":r"^(ALTER(\s*)TABLE(.|\n)*?DROP(\s*)(?!.*PARTITION))",
                                                  "ALTER TABLE RANGE PARTITION":r"^(ALTER(\s*)TABLE(.|\n)*?(RANGE(\s*)PARTITION ))",
                                                  "ALTER TABLE REPLACE COLUMNS":r"^(ALTER(\s*)TABLE(.|\n)*?(REPLACE(\s*)COLUMNS ))",
                                                  "ALTER TABLE RECOVER PARTITIONS":r"^(ALTER(\s*)TABLE(.|\n)*?(RECOVER(\s*)PARTITIONS))",
                                                  "ALTER TABLE SET CACHED IN OR UNCACHED":r"^(ALTER(\s*)TABLE(.|\n)*?SET(\s*)(UNCACHED|CACHED(\s*)IN ))",
                                                  "ALTER TABLE SET ROW FORMAT":r"^(ALTER(\s*)TABLE(.|\n)*?SET(\s*)(ROW(\s*)FORMAT))",
                                                  "ALTER TABLE SET OWNER USER":r"^(ALTER(\s*)TABLE(.|\n)*?(SET(\s*)OWNER(\s*)USER ))",
                                                  "ALTER TABLE WITH STATSKEY":r"^(ALTER(\s*)TABLE(.|\n)*?(numDVs|numNulls|avgSize|maxSize))",
                                                  "ALTER VIEW": r"^(ALTER(\s*)VIEW(.|\n)*?((\((.+)\)(.|\n)*?AS(\s*)SELECT)|COMMENT|SET(\s*)OWNER(\s*)USER ))",
                                                  "COMPUTE STATS":r"^(COMPUTE(.|\n)*?STATS)",
                                                  "COMMENT (START WITH)":r"^(COMMENT)",
                                                  "CREATE FUNCTION":r"^(CREATE(.|\n)*?FUNCTION)",
                                                  "CREATE TABLE EXCEPTIONS":r"^(CREATE(.|\n)*?TABLE(.|\n)*?(PRIMARY(\s*)KEY|FOREIGN(\s*)KEY|SORT(\s*)BY|WITH(\s*)SERDEPROPERTIES|CACHED(\s*)IN ))",
                                                  "CREATE TABLE LIKE":r"^(CREATE(.|\n)*?TABLE(.|\n)*?(LIKE))",
                                                  "CREATE TABLE KUDU EXCEPTIONS":r"^(CREATE(.|\n)*?TABLE(.|\n)*?(PRIMARY(\s*)KEY|NULL|ENCODING|COMPRESSION|DEFAULT|BLOCK_SIZE|PARTITION(\s*)BY ))",
                                                  "CREATE ROLE":r"^(CREATE(\s*)ROLE )",
                                                  "DELETE":r"^(DELETE)",
                                                  "DESCRIBE FORMATTED":r"^(DESCRIBE(.|\n)*?FORMATTED)",
                                                  "DROP FUNCTION":r"^((DROP(\s*)AGGREGATE(\s*)FUNCTION)|DROP(\s*)FUNCTION(.|\n)*?((\((.+)\))))",
                                                  "DROP ROLE":r"^(DROP(\s*)ROLE)",
                                                  "DROP STATS":r"^(DROP(.|\n)*?STATS)",
                                                  "DROP TABLE WITH PURGE":r"^(DROP(\s*)TABLE(.|\n)*?PURGE)",
                                                  "GRANT":r"^(GRANT)",
                                                  "INSERT VALUES":r"^(INSERT(.|\n)*?VALUES)",
                                                  "INVALIDATE METADATA":r"^(INVALIDATE(\s*)METADATA)",
                                                  "OPTIMIZER HINTS":r"(BROADCAST|SHUFFLE|NOSHUFFLE|SCHEDULE_CACHE_LOCAL|SCHEDULE_DISK_LOCAL|SCHEDULE_REMOTE|CLUSTERED|NOCLUSTERED)",
                                                  "REFRESH PARTITION":r"^(REFRESH(.|\n)*?PARTITION)",
                                                  "REFRESH":r"^(REFRESH(\s*)(AUTHORIZATION|FUNCTIONS))",
                                                  "REVOKE":r"^(REVOKE)",
                                                  "SET":r"^(SET)",
                                                  "SHOW FUNCTIONS":r"^(SHOW(\s*)(AGGREGATE|ANALYTIC)(.|\n)*?FUNCTIONS|(SHOW(\s*)FUNCTIONS(\s*)IN ))",
                                                  "SHOW EXCEPTIONS":r"^(SHOW(.|\n)*?(CREATE(\s*)VIEW|GRANT|ROLES|ROLE|FILES(\s*)IN |RANGE|COLUMN(\s*)STATS|TABLE(\s*)STATS))",
                                                  "SHUTDOWN":r"^(:SHUTDOWN)",
                                                  "TRUNCATE":r"^(TRUNCATE)",
                                                  "UPDATE":r"^(UPDATE)",
                                                  "UPSERT":r"^(UPSERT)",
                                                  "VALUES (START WITH)":r"^(VALUES)",
                                                  "WITH INSERT":r"^(WITH(.|\n)*?INSERT)"


                                                },

                                "replace": {
                                                "STRING" : "CHAR",
                                                "STRING" : "VARCHAR"
                                           }
                                

                                 }
                    }
        
    def translate_script(self, script:str)->list:
        """Translate the script to the target language
        :param script: SQL script
        :return: The resulting script + The list of errors + Number of queries
        :rtype: string, list, int
        """
        result = ""
        errors = list()
        command = re.findall("(.*?;)", script, flags=re.DOTALL)
        n_queries = len(command)
        transpiler = Transpiler(from_dialect=self.from_dialect, to_dialect=self.to_dialect)
        regex_key = self.from_dialect + '-' + self.to_dialect
        regex_path = self.regex[regex_key]
        for query in command:
            # Clean comments and remove spaces
            query =  re.sub(r'(--.*?\n)|(/\*(.|\n)*?\*/)', '', query)
            query = query.lstrip()
            #Not Allowed COMMANDS
            if r_not_allowed := re.search("|".join(regex_path["not_allowed"].values()),query, flags= re.IGNORECASE):
                problems = " ".join(r_not_allowed[0].split()[:2])
                logger.warning("Query not supported:\n--STATEMENT:%s",problems)
                result += "\n/* STATEMENT ERRORS:" +problems+ '*/\n' +  query + "\n"
                errors.append([{problems:"HARD:30"}])
            #Select Statments + CTE + Allowed COMMANDS WITH SELECT
            elif r_allowed := re.search('(WITH.*?;)|(SELECT.*?;)', query, flags=re.DOTALL | re.IGNORECASE):
                non_sql = query.replace(r_allowed[0],"") 
                try:
                    _parser = Parser(r_allowed[0])
                    sql, problems = transpiler.translate(_parser)
                    if problems:
                        result += "\n/* TRANSPILER ERRORS: " + str(problems)+ "*/\n" + non_sql + sql + ";" + "\n"
                    else: 
                        result += "\n" + non_sql + sql + ";" + "\n"
                    errors.append(problems)
                except ParseException as err:
                    result += "\n/* PARSER ERRORS: " + str(err) + "*/\n" + query + "\n"
                    errors.append([{"parser":"HARD:30: "+str(err)}])
            else: 
                # Exception that we can deal with replace 
                if r_replace := re.findall("|".join(regex_path['replace'].values()),query, flags = re.IGNORECASE):
                    for item in list(set(r_replace)):
                        key = list(regex_path['replace'].keys())[list(regex_path['replace'].values()).index(item.upper())]
                        query = query.replace(item, key)
                result += "\n" + query + "\n"  
        result += script.split(";")[-1]
        return result, errors, n_queries
    
    def create_folders(self)->str:
        """Create output folders 
        :return: folder paths
        """
        sucess = os.path.join(self.output_dir, "Fully Translated")
        failed = os.path.join(self.output_dir, "Partially Translated")
        if not os.path.exists(sucess) or not os.path.exists(failed):
            os.makedirs(sucess)
            os.makedirs(failed)
        return sucess, failed

    def create_summary(self, errors:list, n_queries:int)->list:
        """Create the script summary
        :param errors: The list of errors that occurred during translation
        :param n_queries: Number of queries per script
        :return: The list with the summary
        """
     
        p_type = [] 
        p_failed = []
        for l in errors:
            for d in l:
                d_key = next(iter(d))
                p_type.append(d_key.lower())
                d_value = d.get(d_key)
                p_desc = d_value.split(":")
                p_failed.append(p_desc[0])
        failed = dict(Counter(p_failed))
        success = n_queries - len(p_failed)
        return [{"N_queries":n_queries},{"Success":success},{"Failed":failed},{"Er_types":p_type}]


    def translate_files(self, summary_dict:bool=False)->dict:
        """Read and translate input directory files 
        :param summary_dict: If true, returns the summary dictionary
        :return:The dictionary with the summary of the files read
        """
        r_summary = dict()
        success, failed = self.create_folders()
        for files in Path(self.input_dir).iterdir():
            if files.is_file():
                f_name = os.path.basename(files)
                with open(files) as f: script = f.read()
                result, errors, n_queries = self.translate_script(script)
                if re.search('(TRANSPILER ERRORS)|(PARSER ERRORS)|(STATEMENT ERRORS)',result):
                    out_path = os.path.join(failed, f_name) 
                    with open(out_path,"w+") as f: script = f.write(result)
                else:
                    out_path = os.path.join(success, f_name) 
                    with open(out_path,"w+") as f: script = f.write(result)
                r_summary[f_name] = self.create_summary(errors, n_queries)
        success_files = len(os.listdir(success))
        failed_files = len(os.listdir(failed))
        f_summary = {"Input_dir" : self.input_dir, "From_dialect": self.from_dialect, "To_dialect":self.to_dialect, "Sucess_files":success_files, "Failed_files":failed_files, "Files" : r_summary}
        Report(f_summary, self.output_dir).generate_report() if self.migration_report else None
        return f_summary if summary_dict else None













                